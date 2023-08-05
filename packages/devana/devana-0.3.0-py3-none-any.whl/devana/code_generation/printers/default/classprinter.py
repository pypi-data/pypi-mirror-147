from devana.code_generation.printers.icodeprinter import ICodePrinter
from devana.code_generation.printers.dispatcherinjectable import DispatcherInjectable
from devana.code_generation.printers.configuration import PrinterConfiguration
from devana.code_generation.printers.formatter import Formatter
from .functionprinter import FunctionPrinter
from .variableprinter import VariablePrinter
from devana.syntax_abstraction.classinfo import *
from typing import Optional


class AccessSpecifierPrinter(ICodePrinter, DispatcherInjectable):

    def print(self, source: AccessSpecifier, config: Optional[PrinterConfiguration] = None, _=None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)
        formatter.print_line(source.value+":")
        return formatter.text


class MethodPrinter(FunctionPrinter):

    def print(self, source: MethodInfo, config: Optional[PrinterConfiguration] = None, _=None) -> str:
        return super().print(source, config)


class ConstructorPrinter(FunctionPrinter):

    def print(self, source: ConstructorInfo, config: Optional[PrinterConfiguration] = None, _=None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)
        if source.associated_comment:
            formatter.print_line(self.printer_dispatcher.print(source.associated_comment, config, source))
        name = source.name
        args = []
        for arg in source.arguments:
            args.append(self.printer_dispatcher.print(arg, config, source))
        args = ", ".join(args)

        template_prefix = ""
        template_suffix = ""
        if source.template:
            parameters = []
            for p in source.template.parameters:
                parameters.append(self.printer_dispatcher.print(p, config, source))
            parameters = ','.join(parameters)
            template_prefix = f"template<{parameters}>"

            specialisation_values = []

            for s in source.template.specialisation_values:
                if type(s) is str:
                    specialisation_values.append(s)
                else:
                    specialisation_values.append(self.printer_dispatcher.print(s, config, source))
            if specialisation_values:
                specialisation_values = ','.join(specialisation_values)
                template_suffix = f"<{specialisation_values}>"

        result = f"{name}{template_suffix}({args})"

        if source.modification.is_static:
            result = "static " + result
        if source.modification.is_inline:
            result = "inline " + result
        if source.modification.is_constexpr:
            result = "constexpr " + result
        if source.modification.is_const:
            result += " const"
        if source.modification.is_volatile:
            result += " volatile"

        if source.modification.is_default:
            result += " = default"
        if source.modification.is_delete:
            result += " = delete"
        if source.modification.is_pure_virtual:
            result = f"virtual {result} = 0"

        if self._is_modification_scope(source):
            if source.modification.is_explicit:
                result = "explicit " + result
            if source.modification.is_final:
                result += " final"
            if source.modification.is_virtual:
                result = "virtual " + result
            if source.modification.is_override:
                result += "override"

        if template_prefix:
            formatter.print_line(template_prefix)

        if source.is_declaration:
            result += ";"
            formatter.line = result
            formatter.next_line()
        else:
            formatter.line = result
            # print initializer list if any
            if source.initializer_list:
                formatter.line += ":"
                formatter.next_line()
                formatter.indent.count += 1
                for i in range(len(source.initializer_list)):
                    init = source.initializer_list[i]
                    formatter.line = f"{init.name}({init.value})"
                    if i != len(source.initializer_list) - 1:
                        formatter.line += ","
                    formatter.next_line()
                formatter.indent.count -= 1
            if not source.initializer_list:
                formatter.next_line()
            formatter.print_line("{")
            formatter.indent.count += 1
            for line in source.body.splitlines(False):
                formatter.print_line(line)
            formatter.indent.count -= 1
            formatter.print_line("}")
        return formatter.text


class DestructorPrinter(FunctionPrinter):

    def print(self, source: DestructorInfo, config: Optional[PrinterConfiguration] = None, _=None) -> str:
        return super().print(source, config)


class FieldPrinter(VariablePrinter):

    def print(self, source: FieldInfo, config: Optional[PrinterConfiguration] = None, context: Optional = None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)
        if source.associated_comment:
            formatter.print_line(self.printer_dispatcher.print(source.associated_comment, config, source))
        formatter.print_line(super().print(source, config, context) + ";")
        return formatter.text


class ClassPrinter(ICodePrinter, DispatcherInjectable):

    def print(self, source: ClassInfo, config: Optional[PrinterConfiguration] = None, context: Optional = None) -> str:
        if config is None:
            config = PrinterConfiguration()
        formatter = Formatter(config)
        if type(context) is TypeExpression or type(context) is InheritanceInfo.InheritanceValue:
            return source.name
        else:

            if source.associated_comment:
                formatter.print_line(self.printer_dispatcher.print(source.associated_comment, config, source))

            template_prefix = ""
            template_suffix = ""
            if source.template:
                parameters = []
                for p in source.template.parameters:
                    parameters.append(self.printer_dispatcher.print(p, config, source))
                parameters = ','.join(parameters)
                template_prefix = f"template<{parameters}>"

                specialisation_values = []

                for s in source.template.specialisation_values:
                    if type(s) is str:
                        specialisation_values.append(s)
                    else:
                        specialisation_values.append(self.printer_dispatcher.print(s, config, source))
                if specialisation_values:
                    specialisation_values = ','.join(specialisation_values)
                    template_suffix = f"<{specialisation_values}>"

            if template_prefix:
                formatter.print_line(template_prefix)

            formatter.line = "class" if source.is_class else "struct"
            formatter.line += f" {source.name}" + template_suffix
            if source.is_declaration:
                formatter.line += ";"
                formatter.next_line()
            else:
                if source.inheritance:
                    formatter.line += ": "
                    if source.inheritance:
                        parents = []
                        for i in range(len(source.inheritance.type_parents)):
                            parent = source.inheritance.type_parents[i]
                            value = f"{parent.access_specifier.value} "
                            if parent.is_virtual:
                                value += "virtual "
                            value += self.printer_dispatcher.print(parent.type, config,
                                                                   InheritanceInfo.InheritanceValue())
                            parents.append(value)
                        formatter.line += ", ".join(parents)
                formatter.next_line()
                formatter.print_line("{")
                formatter.indent.count += 1
                for element in source.content:
                    formatter.line += self.printer_dispatcher.print(element, config, source)
                formatter.accumulate_line()
                formatter.indent.count -= 1
                formatter.print_line("};")
            return formatter.text
