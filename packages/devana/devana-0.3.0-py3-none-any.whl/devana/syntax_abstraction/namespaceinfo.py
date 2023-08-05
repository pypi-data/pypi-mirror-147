from devana.syntax_abstraction.organizers.codecontainer import CodeContainer
from typing import Optional, List
from devana.syntax_abstraction.codepiece import CodePiece
from clang import cindex
from devana.syntax_abstraction.functioninfo import FunctionInfo
from devana.syntax_abstraction.comment import Comment
from devana.utility.errors import ParserError
from devana.utility.lazy import LazyNotInit, lazy_invoke
from devana.syntax_abstraction.organizers.lexicon import Lexicon


class NamespaceInfo(CodeContainer):
    """"Object representation of current scope namespace, for example usage in file or global namespace with all
    namespaces component placed in many files."""

    def __init__(self, cursor: Optional[cindex.Cursor] = None, parent: Optional[CodeContainer] = None):
        super().__init__(cursor, parent)
        if cursor is None:
            self._text_source = None
            self._name = ""
            self._associated_comment = None
        else:
            if self._cursor.kind != cindex.CursorKind.NAMESPACE:
                raise ParserError("It is not a valid type cursor.")
            self._text_source = LazyNotInit
            self._name = LazyNotInit
            self._associated_comment = LazyNotInit
        self._lexicon = Lexicon.create(self)

    @property
    @lazy_invoke
    def name(self) -> str:
        self._name = self._cursor.displayname
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def text_source(self) -> Optional[CodePiece]:
        """Source of this element."""
        self._text_source = CodePiece(self._cursor)
        return self._text_source

    @property
    def lexicon(self) -> Lexicon:
        return self._lexicon

    @lexicon.setter
    def lexicon(self, value):
        self._lexicon = value

    @property
    @lazy_invoke
    def associated_comment(self) -> Optional[Comment]:
        parent = self.parent
        while parent is not None:
            if hasattr(parent, "bind_comment"):
                self._associated_comment = parent.bind_comment(self)
                return self._associated_comment
            parent = parent.parent

        return None

    @associated_comment.setter
    def associated_comment(self, value):
        self._associated_comment = value

    def _create_content(self) -> List[any]:
        from devana.syntax_abstraction.usingnamespace import UsingNamespace
        from devana.syntax_abstraction.classinfo import ClassInfo, MethodInfo
        from devana.syntax_abstraction.enuminfo import EnumInfo
        from devana.syntax_abstraction.typedefinfo import TypedefInfo
        from devana.syntax_abstraction.variable import GlobalVariable
        from devana.syntax_abstraction.unioninfo import UnionInfo
        from devana.syntax_abstraction.externc import ExternC
        types = [FunctionInfo, NamespaceInfo, UsingNamespace, ClassInfo, EnumInfo, TypedefInfo, MethodInfo, UnionInfo,
                 GlobalVariable, ExternC]
        content = []
        for children in self._cursor.get_children():
            for t in types:
                try:
                    el = t(children, self)
                except ValueError:
                    continue
                content.append(el)
                break
        return content
