r""" ccp_abc.py - Parse, Query, Build, and Modify IOS-style configurations
     Copyright (C) 2022-2023 David Michael Pennington
     Copyright (C) 2022 David Michael Pennington at WellSky
     Copyright (C) 2020-2021 David Michael Pennington at Cisco Systems
     Copyright (C) 2019      David Michael Pennington at ThousandEyes
     Copyright (C) 2014-2019 David Michael Pennington at Samsung Data Services
     This program is free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.
     This program is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.
     You should have received a copy of the GNU General Public License
     along with this program.  If not, see <http://www.gnu.org/licenses/>.
     If you need to contact the author, you can do so by emailing:
     mike [~at~] pennington [/dot\] net
"""

from abc import ABCMeta
import warnings
import inspect
import re

from ciscoconfparse.errors import InvalidTypecast, InvalidParameters
from ciscoconfparse.ccp_util import junos_unsupported
from loguru import logger

DEFAULT_TEXT = "__undefined__"

#
# -------------  Config Line ABC
#
class BaseCfgLine(metaclass=ABCMeta):
    comment_delimiter = None
    _uncfgtext_to_be_deprecated = ""
    _text = DEFAULT_TEXT
    linenum = -1
    parent = None
    child_indent = 0
    is_comment = None
    children = []
    indent = 0  # assign indent in the self.text setter method
    confobj = None  # Reference to the list object which owns it
    blank_line_keep = False  # CiscoConfParse() uses blank_line_keep

    all_text = []
    text = DEFAULT_TEXT  # Use self.text setter method to set this value

    _line_id = None
    diff_rendered = None
    diff_linenum = -1
    _diff_word = ""  # diff_word: 'keep', 'remove', 'unchanged', 'add'
    _diff_side = ""  # diff_side: 'before', 'after' or ''

    # deprecating py2.foo metaclass syntax in version 1.6.8...
    # __metaclass__ = ABCMeta
    @logger.catch(reraise=True)
    def __init__(self, all_lines=None, line=DEFAULT_TEXT, comment_delimiter="!", **kwargs):
        """Accept an IOS line number and initialize family relationship attributes"""

        # Hack to accept old parameter names instead of finding all the places
        # where `all_text` and `text` are used and renaming attributes all
        # over the place
        if isinstance(kwargs.get("all_text", None), list):
            all_lines = kwargs.get("all_text")
        if isinstance(kwargs.get("text", None), str):
            line = kwargs.get("text")

        self.comment_delimiter = comment_delimiter
        self._uncfgtext_to_be_deprecated = ""
        self._text = DEFAULT_TEXT
        self.linenum = -1
        self.parent = self  # by default, assign parent as itself
        self.child_indent = 0
        self.is_comment = None
        self.children = []
        self.indent = 0  # assign indent in the self.text setter method
        self.confobj = None  # Reference to the list object which owns it
        self.blank_line_keep = False  # CiscoConfParse() uses blank_line_keep

        # Call set_comment_bool() in the self.text setter method...
        self.all_text = all_lines
        self.text = line  # Use self.text setter method to set this value

        self._line_id = None
        self.diff_rendered = None
        self.diff_linenum = -1
        self._diff_word = ""  # diff_word: 'keep', 'remove', 'unchanged', 'add'
        self._diff_side = ""  # diff_side: 'before', 'after' or ''

        # FIXME
        #   Bypass @text.setter method for now...  @text.setter writes to
        #   self._text, but currently children do not associate correctly if
        #   @text.setter is used as-is...
        # self.text = text

    # On BaseCfgLine()
    @logger.catch(reraise=True)
    def __repr__(self):
        try:
            parent_linenum = self.parent.linenum
        except AttributeError:
            parent_linenum = self.linenum

        if not self.is_child:
            return "<{} # {} '{}'>".format(self.classname, self.linenum, self.text)
        else:
            return "<{} # {} '{}' (parent is # {})>".format(
                self.classname,
                self.linenum,
                self.text,
                parent_linenum,
            )

    # On BaseCfgLine()
    @logger.catch(reraise=True)
    def __str__(self):
        return self.__repr__()

    # On BaseCfgLine()
    @logger.catch(reraise=True)
    def __len__(self):
        return len(self.text)

    # On BaseCfgLine()
    @logger.catch(reraise=True)
    def __hash__(self):
        ##   I inlined the hash() argument below for speed... whenever I change
        ##   self.__eq__() I *must* change this
        return hash(str(self.linenum) + self.text)

    # On BaseCfgLine()
    @logger.catch(reraise=True)
    def __getattr__(self, attr):
        try:
            retval = getattr(object, attr)
            return retval
        except BaseException:
            error = f"The {attr} attribute does not exist"
            logger.error(error)
            raise AttributeError(error)

    # On BaseCfgLine()
    @logger.catch(reraise=True)
    def __eq__(self, val):
        try:
            ##   try / except is much faster than isinstance();
            ##   I added hash_arg() inline below for speed... whenever I change
            ##   self.__hash__() I *must* change this
            # FIXME
            return hash(str(self.linenum) + self.text) == hash(
                str(val.linenum) + val.text
            )
        except Exception:
            return False

    # On BaseCfgLine()
    @logger.catch(reraise=True)
    def __gt__(self, val):
        if self.linenum > val.linenum:
            return True
        return False

    # On BaseCfgLine()
    @logger.catch(reraise=True)
    def __lt__(self, val):
        # Ref: http://stackoverflow.com/a/7152796/667301
        if self.linenum < val.linenum:
            return True
        return False

    # On BaseCfgLine()
    @property
    @logger.catch(reraise=True)
    def is_intf(self):
        """subclasses will override this method"""
        raise NotImplementedError()

    # On BaseCfgLine()
    @is_intf.setter
    @logger.catch(reraise=True)
    def is_intf(self, value):
        raise NotImplementedError()

    # On BaseCfgLine()
    @property
    @logger.catch(reraise=True)
    def is_subintf(self):
        """subclasses will override this method"""
        raise NotImplementedError()

    # On BaseCfgLine()
    @is_subintf.setter
    @logger.catch(reraise=True)
    def is_subintf(self, value):
        raise NotImplementedError()

    # On BaseCfgLine()
    @property
    @logger.catch(reraise=True)
    def is_switchport(self):
        """subclasses will override this method"""
        raise NotImplementedError()

    # On BaseCfgLine()
    @is_switchport.setter
    @logger.catch(reraise=True)
    def is_switchport(self, value):
        raise NotImplementedError()

    # On BaseCfgLine()
    @logger.catch(reraise=True)
    def set_comment_bool(self):
        """Set the .is_comment attribute for this object."""
        delimiters = set(self.comment_delimiter)
        ## Use this instead of a regex... nontrivial speed enhancement
        tmp = self.text.lstrip()
        for delimit_char in delimiters:
            if len(tmp) > 0 and (delimit_char == tmp[len(delimit_char) - 1]):
                self.is_comment = True
                break
            else:
                self.is_comment = False
        return self.is_comment

    # On BaseCfgLine()
    @property
    @logger.catch(reraise=True)
    def index(self):
        """Alias index to linenum"""
        return self.linenum

    # On BaseCfgLine()
    @logger.catch(reraise=True)
    def calculate_line_id(self):
        """
        Calculate and return an integer line_id for BaseCfgLine()

        The `hash()` of `self.text` is used to build a numerical identity
        for a given BaseCfgLine().

        Do NOT cache this value.  It must be recalculated when self._text
        changes.
        """
        indent = self.indent

        # Do NOT make changes to _line_id.  This hash() value built from
        #     _line_id is the glue that holds `ciscoconfparse.HDiff()`
        #     together.
        _line_id = hash(" " * indent + " ".join(self.text.strip().split()))

        if bool([]): # Do not execute this code...
            ##################################################################
            # use str.split() below to ensure that whitespace differences
            #     hash the same way... I added this code as a possible
            #     implementation for github issue #266... however, after
            #     using this new code, I decided that it makes HDiff()
            #     too complicated.
            #
            # I am keeping this in calculate_line_id() to document the
            #     proposal and why I decided against it.
            ##################################################################
            indent_str = indent * " "
            if self.is_comment is False:
                _line_id = hash(indent_str + " ".join(self.text.strip().split()))
            elif self.is_comment is True:
                _line_id = hash(indent_str + " ".join((str(self.linenum) + " " + self.text.strip()).split()))
            elif self.text.strip() == "":
                _line_id = hash(str(self.linenum))
            else:
                raise NotImplementedError(self.text)

        return _line_id

    # On BaseCfgLine()
    @property
    @logger.catch(reraise=True)
    def diff_id_list(self):
        """
        Return a list of integers as a context-sensitive diff identifier.

        The returned value includes line_id of all parents.  The oldest
        ancestor / parent line_id is last in the returned list of line_id
        hash values.

        object id integers are NOT the same between script runs.
        """
        retval = []
        len_geneology = len(self.geneology)

        for idx, obj in enumerate(self.geneology):
            # W0212: Access to a protected attribute (i.e. with leading underscore)
            obj._line_id = obj.calculate_line_id() # noqa: W0212

            # idx = 0 is the oldest ancestor
            if idx == 0:
                # This object is NOT a child
                retval.insert(0, obj._line_id)

            elif idx <= len_geneology - 1:
                # This object is a child of self.parent
                retval.insert(0, obj._line_id)

        # retval usually looks like this (example with a single parent obj):
        #
        #                          [-1387406312585020591, 3965133112392387338]
        #  root / oldest _line_id:                        ^^^^^^^^^^^^^^^^^^^
        #  child object _line_id:   ^^^^^^^^^^^^^^^^^^^^
        return retval

    # On BaseCfgLine()
    @property
    @logger.catch(reraise=True)
    def diff_word(self):
        """A diff_word getter attribute (typically used in HDiff())"""
        return self._diff_word

    # On BaseCfgLine()
    @diff_word.setter
    @logger.catch(reraise=True)
    def diff_word(self, val):
        """A diff_word setter attribute (typically used in HDiff())"""

        # Check against expected HDiff() values...
        if self.diff_side == "before":
            assert val in set(
                {
                    "keep",
                    "remove",
                    "",
                }
            )

        elif self.diff_side == "after":
            assert val in set(
                {
                    "unchanged",
                    "add",
                    "unknown",
                    "",
                }
            )

        else:
            raise ValueError("diff_side can only be 'before' or 'after'")
        self._diff_word = val

    # On BaseCfgLine()
    @property
    @logger.catch(reraise=True)
    def diff_side(self):
        """A diff_side getter attribute (typically used in HDiff())"""
        return self._diff_side

    # On BaseCfgLine()
    @diff_side.setter
    @logger.catch(reraise=True)
    def diff_side(self, val):
        """A diff_side setter attribute (typically used in HDiff())"""
        assert val in set(
            {
                "before",
                "after",
                "",
            }
        )
        self._diff_side = val

    # On BaseCfgLine()
    @property
    @logger.catch(reraise=True)
    def as_diff_dict(self):
        """An internal dict which is used in :class:`~ciscoconfparse.HDiff()`"""
        retval = {
            "linenum": self.diff_linenum,
            "diff_side": self.diff_side,
            "diff_word": self.diff_word,
            "indent": self.indent,
            "parents": [ii.text for ii in self.all_parents],
            "text": self.text,
            "diff_id_list": self.diff_id_list,
        }
        return retval

    # On BaseCfgLine()
    @property
    @logger.catch(reraise=True)
    def text(self):
        """Get the self.text attribute"""
        return self._text

    # On BaseCfgLine()
    @text.setter
    @logger.catch(reraise=True)
    def text(self, newtext=None):
        """Set self.text, self.indent, self.line_id (and all comments' self.parent)"""
        # FIXME - children do not associate correctly if this is used as-is...
        if not isinstance(newtext, str):
            error = f"text=`{newtext}` is an invalid config line"
            logger.critical(error)
            raise InvalidParameters(error)

        # escape braces since single braces could be misunderstood as
        # f-string or string.format() delimiters...
        #
        # Sometimes brace escaping is not required... we need better fencing
        # around safe_escape_curly_braces()
        if False:
            newtext = self.safe_escape_curly_braces(newtext)

        # Calculate the newtext indent here...
        newtext_ = newtext.rstrip()
        _newtext_ = newtext_.lstrip()
        self.indent = len(newtext_) - len(_newtext_)

        # Remove all double-spacing, except for the indent spaces...
        # self._text = self.indent * " " + " ".join([ii.strip() for ii in _newtext_.split()])
        self._text = newtext_
        self.line_id = self.calculate_line_id()

        self.set_comment_bool()
        if self.is_comment is True:
            # VERY IMPORTANT: due to old behavior, comment parents MUST be self
            #
            self.parent = self

    # On BaseCfgLine()
    @logger.catch(reraise=True)
    def safe_escape_curly_braces(self, text):
        """
        Escape curly braces in strings since they could be misunderstood as
        f-string or string.format() delimiters...

        If BaseCfgLine receives line with curly-braces, this method can
        escape the curly braces so they are not mis-interpreted as python
        string formatting delimiters.
        """
        # Bypass escaping curly braces if there aren't any...
        if not ("{" in text) and not ("}" in text):
            return text

        assert ("{" in text) or ("}" in text)

        # Skip escaping curly braces if text already has double curly braces...
        if ("{{" in text) or ("}}" in text):
            return text

        text = text.replace("{", "{{")
        text = text.replace("}", "}}")
        return text

    # On BaseCfgLine()
    @property
    def line_id(self):
        return self._line_id

    # On BaseCfgLine()
    @line_id.setter
    def line_id(self, value=None):
        assert isinstance(value, int)
        self._line_id = value

    # On BaseCfgLine()
    @property
    def dna(self):
        return self.classname

    # On BaseCfgLine()
    @property
    def hash_children(self):
        """Return a unique hash of all children (if the number of children > 0)"""
        if len(self.all_children) > 0:
            return hash(tuple(self.all_children))
        else:
            return hash(())

    # On BaseCfgLine()
    @property
    def family_endpoint(self):
        assert isinstance(self.all_children, list)
        if self.all_children == []:
            # CHANGED on 2022-04-01... PREVIOUS_VALUE="return 0"
            # CHANGED on 2022-04-01... NEW_VALUE="self.linenum"
            return self.linenum
        else:
            return self.all_children[-1].linenum

    # On BaseCfgLine()
    @property
    def verbose(self):
        if self.has_children:
            return (
                "<%s # %s '%s' (child_indent: %s / len(children): %s / family_endpoint: %s)>"
                % (
                    self.classname,
                    self.linenum,
                    self.text,
                    self.child_indent,
                    len(self.children),
                    self.family_endpoint,
                )
            )
        else:
            return "<{} # {} '{}' (no_children / family_endpoint: {})>".format(
                self.classname,
                self.linenum,
                self.text,
                self.family_endpoint,
            )

    # On BaseCfgLine()
    @property
    def all_parents(self):
        retval = set()
        me = self
        while me.parent != me:
            retval.add(me.parent)
            me = me.parent
        return sorted(retval)

    # On BaseCfgLine()
    @property
    def all_children(self):
        retval = set()
        if self.has_children:
            for child in self.children:
                retval.add(child)
                retval.update(child.all_children)
        return sorted(retval)

    # On BaseCfgLine()
    @property
    def classname(self):
        return self.__class__.__name__

    # On BaseCfgLine()
    @property
    def has_children(self):
        if len(self.children) > 0:
            return True
        return False

    # On BaseCfgLine()
    @property
    def is_config_line(self):
        """
        Return a boolean for whether this is a config statement; returns False
        if this object is a blank line, or a comment.
        """
        if len(self.text.strip()) > 0 and not self.is_comment:
            return True
        return False

    # On BaseCfgLine()
    def _list_reassign_linenums(self):
        # Call this when I want to reparse everything
        #     (which is very slow)
        # NOTE - 1.5.30 removed this method (which was only called
        #     by confobj.delete()) in favor of a simpler approach
        #     in confobj.delete()
        #
        raise NotImplementedError()

    # On BaseCfgLine()
    @junos_unsupported
    def add_parent(self, parentobj):
        """Add a reference to parentobj, on this object"""
        ## In a perfect world, I would check parentobj's type
        ##     with isinstance(), but I'm not ready to take the perf hit
        self.parent = parentobj
        return True

    # On BaseCfgLine()
    @junos_unsupported
    def add_child(self, childobj):
        """Add references to childobj, on this object"""
        ## In a perfect world, I would check childobj's type
        ##     with isinstance(), but I'm not ready to take the perf hit
        ##
        ## Add the child, unless we already know it
        if not (childobj in self.children):
            self.children.append(childobj)
            self.child_indent = childobj.indent
            return True
        else:
            return False

    # On BaseCfgLine()
    @junos_unsupported
    def add_uncfgtext(self, unconftext=None):
        """
        add_uncfgtext() is deprecated and will be removed.

        .. code-block:: python
           :emphasize-lines: 16
           >>> # assume parse.find_objects() returned a value in obj below
           >>> obj.text
           ' no ip proxy-arp'
           >>> obj.uncfgtext
           ''
           >>> obj.add_uncfgtext(" no ip proxy-arp")
        """
        assert isinstance(unconftext, str)
        assert isinstance(self.text, str) and self.text != DEFAULT_TEXT

        # adding a deprecation warning in version 1.7.0...
        deprecation_warn_str = "add_uncfgtext() is deprecated and will be removed."
        warnings.warn(deprecation_warn_str, DeprecationWarning)
        ## remove any preceeding "no " from Cisco IOS commands...
        conftext = re.sub(r"^(\s*)(no\s+)(\S.*)?$", "\3", unconftext)
        myindent = self.parent.child_indent

        # write access to self.uncfgtext is not supported
        self._uncfgtext_to_be_deprecated = myindent * " " + "no " + conftext

    @property
    def uncfgtext(self):
        """
        Return a 'best-effort' Cisco IOS-style config to remove this
        configuration object.

        This `uncfgtext` string should not be considered correct
        in all Cisco IOS command unconfigure cases.
        """
        assert isinstance(self.text, str) and self.text != DEFAULT_TEXT

        tmp = [ii.strip() for ii in self.text.split()]

        # _uncfgtext_to_be_deprecated is normally set in add_uncfgtext()...
        # deprecation warnings for _uncfgtext_to_be_deprecated were
        # introduced in version 1.7.0...
        if self._uncfgtext_to_be_deprecated != "":
            # Officially, _uncfgtext_to_be_deprecated is not supported.
            # This if-case is here for someone who may have set
            # self.uncfgtext in older ciscoconfparse versions.
            #
            # After uncfgtext.setter (below) is removed, we can rip out
            # this portion of the if-else logic...
            deprecation_warn_str = "add_uncfgtext() is deprecated and will be removed."
            warnings.warn(deprecation_warn_str, DeprecationWarning)
            return self._uncfgtext_to_be_deprecated

        # Once _uncfgtext_to_be_deprecated is removed, we can make this
        # condition the first in this if-else logic...
        elif tmp[0].lower() == "no":
            assert len(tmp) > 1  # join() below only makes sense if len(tmp)>1
            return self.indent * " " + " ".join(tmp[1:])

        else:
            return self.indent * " " + "no " + self.text.lstrip()

    @uncfgtext.setter
    def uncfgtext(self, value=""):
        # Officially, _uncfgtext_to_be_deprecated is not supported. This
        # setter is here for someone who may have set self.uncfgtext in older
        # ciscoconfparse versions.
        #
        # This uncfgtext setter was added in version 1.7.0...
        deprecation_warn_str = "setting uncfgtext is deprecated and will be removed."
        warnings.warn(deprecation_warn_str, DeprecationWarning)

        self._uncfgtext_to_be_deprecated = value

    # On BaseCfgLine()
    @junos_unsupported
    def delete(self, recurse=True):
        """Delete this object.  By default, if a parent object is deleted, the child objects are also deleted; this happens because ``recurse`` defaults True."""
        if self.confobj.debug >= 1:
            logger.info("{}.delete(recurse={}) was called.".format(self, recurse))

        # Build a set of all IOSCfgLine() object instances to be deleted...
        delete_these = set(
            {
                self,
            }
        )

        if recurse is True:
            if self.confobj.debug >= 1:
                logger.debug(
                    "Executing <IOSCfgLine line #{}>.delete(recurse=True)".format(
                        self.linenum
                    )
                )

            # NOTE - 1.5.30 changed this from iterating over self.children
            #        to self.all_children
            for child in self.all_children:
                delete_these.add(child)

            # reverse is important here so we can delete a range of line numbers
            # without clobbering the line numbers that haven't been deleted
            # yet...
            for obj in sorted(delete_these, reverse=True):
                linenum = obj.linenum
                if self.confobj.debug >= 1:
                    logger.debug(
                        "    Deleting <IOSCfgLine(line # {})>.".format(linenum)
                    )
                del self.confobj._list[linenum]

        else:
            if self.confobj.debug >= 1:
                logger.debug(
                    "Executing <IOSCfgLine line #{}>.delete(recurse=False)".format(
                        self.linenum
                    )
                )
            ## Consistency check to refuse deletion of the wrong object...
            ##    only delete if the line numbers are consistent
            text = self.text
            linenum = self.linenum
            assert self.confobj._list[linenum].text == text

            if self.confobj.debug >= 1:
                logger.debug("    Deleting <IOSCfgLine(line # {})>.".format(linenum))
            del self.confobj._list[linenum]

        self.confobj.reassign_linenums()
        return True

    # On BaseCfgLine()
    @junos_unsupported
    def delete_children_matching(self, linespec):
        """Delete any child :class:`~models_cisco.IOSCfgLine` objects which
        match ``linespec``.
        Parameters
        ----------
        linespec : str
            A string or python regular expression, which should be matched.
        Returns
        -------
        list
            A list of :class:`~models_cisco.IOSCfgLine` objects which were deleted.
        Examples
        --------
        This example illustrates how you can use
        :func:`~ccp_abc.delete_children_matching` to delete any description
        on an interface.
        .. code-block:: python
           :emphasize-lines: 16
           >>> from ciscoconfparse import CiscoConfParse
           >>> config = [
           ...     '!',
           ...     'interface Serial1/0',
           ...     ' description Some lame description',
           ...     ' ip address 1.1.1.1 255.255.255.252',
           ...     '!',
           ...     'interface Serial1/1',
           ...     ' description Another lame description',
           ...     ' ip address 1.1.1.5 255.255.255.252',
           ...     '!',
           ...     ]
           >>> parse = CiscoConfParse(config)
           >>>
           >>> for obj in parse.find_objects(r'^interface'):
           ...     obj.delete_children_matching(r'description')
           >>>
           >>> for line in parse.ioscfg:
           ...     print(line)
           ...
           !
           interface Serial1/0
            ip address 1.1.1.1 255.255.255.252
           !
           interface Serial1/1
            ip address 1.1.1.5 255.255.255.252
           !
           >>>
        """
        # if / else in a list comprehension... ref ---> https://stackoverflow.com/a/9442777/667301
        retval = [
            (obj.delete() if obj.re_search(linespec) else obj) for obj in self.children
        ]
        return retval

    # On BaseCfgLine()
    def has_child_with(self, linespec, all_children=False):
        assert isinstance(all_children, bool)
        # Old, crusty broken... fixed in 1.6.30...
        # return bool(filter(methodcaller("re_search", linespec), self.children))
        #
        # TODO - check whether using re_match_iter_typed() is faster than this:
        ll = linespec
        if all_children is False:
            offspring = self.children
        else:
            offspring = self.all_children
        return bool(len([ll for cobj in offspring if cobj.re_search(ll)]))

    # On BaseCfgLine()
    @junos_unsupported
    def insert_before(self, insertstr=None):
        """
        Usage:
        confobj.insert_before('! insert text before this confobj')
        """
        retval = None
        calling_fn_index = 1
        calling_filename = inspect.stack()[calling_fn_index].filename
        calling_function = inspect.stack()[calling_fn_index].function
        calling_lineno = inspect.stack()[calling_fn_index].lineno
        error = "FATAL CALL: in {} line {} {}(insertstr='{}')".format(
            calling_filename, calling_lineno, calling_function, insertstr
        )
        if isinstance(insertstr, str) is True:
            retval = self.confobj.insert_before(exist_val=self.text, new_val=insertstr, atomic=False)

        elif isinstance(insertstr, BaseCfgLine) is True:
            retval = self.confobj.insert_before(exist_val=self.text, new_val=insertstr.text, atomic=False)

        else:
            raise ValueError(error)

        # retval = self.confobj.insert_after(self, insertstr, atomic=False)
        return retval

    # On BaseCfgLine()
    @junos_unsupported
    def insert_after(self, insertstr=None):
        """Usage:
        confobj.insert_after('! insert text after this confobj')"""

        # Fail if insertstr is not the correct object type...
        #   only strings and *CfgLine() are allowed...
        if not isinstance(insertstr, str) and not isinstance(insertstr, "BaseCfgLine"):
            error = "Cannot insert object type - %s" % type(insertstr)
            logger.error(error)
            raise NotImplementedError(error)

        retval = None
        calling_fn_index = 1
        calling_filename = inspect.stack()[calling_fn_index].filename
        calling_function = inspect.stack()[calling_fn_index].function
        calling_lineno = inspect.stack()[calling_fn_index].lineno
        if self.confobj.debug >= 1:
            logger.debug("Inserting '{}' after '{}'".format(insertstr, self))

        if isinstance(insertstr, str) is True:
            # Handle insertion of a plain-text line
            retval = self.confobj.insert_after(exist_val=self.text, new_val=insertstr, atomic=False)

        elif isinstance(insertstr, "BaseCfgLine"):
            # Handle insertion of a configuration line obj such as IOSCfgLine()
            retval = self.confobj.insert_after(exist_val=self.text, new_val=insertstr.text, atomic=False)

        else:
            error = "FATAL CALL: in {} line {} {}(insertstr='{}')".format(
                calling_filename, calling_lineno, calling_function, insertstr
            )
            logger.error(error)
            raise ValueError(error)

        # retval = self.confobj.insert_after(self, insertstr, atomic=False)
        return retval

    # On BaseCfgLine()
    @junos_unsupported
    def append_to_family(
        self, insertstr, indent=-1, auto_indent_width=1, auto_indent=False
    ):
        """Append an :class:`~models_cisco.IOSCfgLine` object with ``insertstr``
        as a child at the bottom of the current configuration family.
        Parameters
        ----------
        insertstr : str
            A string which contains the text configuration to be apppended.
        indent : int
            The amount of indentation to use for the child line; by default, the number of left spaces provided with ``insertstr`` are respected.  However, you can manually set the indent level when ``indent``>0.  This option will be ignored, if ``auto_indent`` is True.
        auto_indent_width : int
            Amount of whitespace to automatically indent
        auto_indent : bool
            Automatically indent the child to ``auto_indent_width``
        Returns
        -------
        str
            The text matched by the regular expression group; if there is no match, None is returned.
        Examples
        --------
        This example illustrates how you can use
        :func:`~ccp_abc.append_to_family` to add a
        ``carrier-delay`` to each interface.
        .. code-block:: python
           :emphasize-lines: 14
           >>> from ciscoconfparse import CiscoConfParse
           >>> config = [
           ...     '!',
           ...     'interface Serial1/0',
           ...     ' ip address 1.1.1.1 255.255.255.252',
           ...     '!',
           ...     'interface Serial1/1',
           ...     ' ip address 1.1.1.5 255.255.255.252',
           ...     '!',
           ...     ]
           >>> parse = CiscoConfParse(config)
           >>>
           >>> for obj in parse.find_objects(r'^interface'):
           ...     obj.append_to_family(' carrier-delay msec 500')
           ...
           >>> parse.commit()
           >>>
           >>> for line in parse.ioscfg:
           ...     print(line)
           ...
           !
           interface Serial1/0
            ip address 1.1.1.1 255.255.255.252
            carrier-delay msec 500
           !
           interface Serial1/1
            ip address 1.1.1.5 255.255.255.252
            carrier-delay msec 500
           !
           >>>
        """
        ## Build the string to insert with proper indentation...
        if auto_indent:
            insertstr = (" " * (self.indent + auto_indent_width)) + insertstr.lstrip()
        elif indent > 0:
            insertstr = (" " * (self.indent + indent)) + insertstr.lstrip()
        ## BaseCfgLine.append_to_family(), insert a single line after this
        ##  object's children
        try:
            last_child = self.all_children[-1]
            retval = self.confobj.insert_after(last_child, insertstr, atomic=False)
        except IndexError:
            # The object has no children
            retval = self.confobj.insert_after(self, insertstr, atomic=False)
        return retval

    # On BaseCfgLine()
    @junos_unsupported
    def replace(self, linespec, replacestr, ignore_rgx=None):
        """Replace all strings matching ``linespec`` with ``replacestr`` in
        the :class:`~models_cisco.IOSCfgLine` object; however, if the
        :class:`~models_cisco.IOSCfgLine` text matches ``ignore_rgx``, then
        the text is *not* replaced.  The ``replace()`` method is simply an
        alias to the ``re_sub()`` method.
        Parameters
        ----------
        linespec : str
            A string or python regular expression, which should be matched
        replacestr : str
            A string or python regular expression, which should replace the text matched by ``linespec``.
        ignore_rgx : str
            A string or python regular expression; the replacement is skipped if :class:`~models_cisco.IOSCfgLine` text matches ``ignore_rgx``.  ``ignore_rgx`` defaults to None, which means no lines matching ``linespec`` are skipped.
        Returns
        -------
        str
            The new text after replacement
        Examples
        --------
        This example illustrates how you can use
        :func:`~models_cisco.IOSCfgLine.replace` to replace ``Serial1`` with
        ``Serial0`` in a configuration...
        .. code-block:: python
           :emphasize-lines: 15
           >>> from ciscoconfparse import CiscoConfParse
           >>> config = [
           ...     '!',
           ...     'interface Serial1/0',
           ...     ' ip address 1.1.1.1 255.255.255.252',
           ...     '!',
           ...     'interface Serial1/1',
           ...     ' ip address 1.1.1.5 255.255.255.252',
           ...     '!',
           ...     ]
           >>> parse = CiscoConfParse(config)
           >>>
           >>> for obj in parse.find_objects('Serial'):
           ...     print("OLD {}".format(obj.text))
           ...     obj.replace(r'Serial1', r'Serial0')
           ...     print("  NEW {}".format(obj.text))
           OLD interface Serial1/0
             NEW interface Serial0/0
           OLD interface Serial1/1
             NEW interface Serial0/1
           >>>
        """
        # This is a little slower than calling BaseCfgLine.re_sub directly...
        return self.re_sub(linespec, replacestr, ignore_rgx)

    # On BaseCfgLine()
    @logger.catch(reraise=True)
    def get_typed_dict(self, regex=None, type_dict=None, default=None, debug=False):
        """Return a typed dict if `regex` is an re.Match() instance and `type_dict` is a `dict` of types.  If a key in `type_dict` does not match, `default` is returned for that key.

        Examples
        --------
        These examples demonstrate how ``get_typed_dict()`` works.

        .. code-block:: python
           >>> _uut_regex = r"^(?P<my_digit>[\d+])(?P<no_digit>[^\d+])"
           >>> _type_dict = {"my_digit", int, "no_digit": str}
           >>> _default = "_no_match"
           >>> get_typed_dict(re.search(_uut_regex, "1a"), type_dict=_type_dict, default=_default)
           {'my_digit': 1, 'no_digit': 'a'}
           >>> get_typed_dict(re.search(_uut_regex, "a1"), type_dict=_type_dict, default=_default)
           {'my_digit': '_no_match', 'no_digit': '_no_match'}
           >>> get_typed_dict(re.search(_uut_regex, ""), type_dict=_type_dict, default=_default)
           {'my_digit': '_no_match', 'no_digit': '_no_match'}
           >>>

        """
        retval = {}
        if debug is True:
            logger.info(f"{self}.get_typed_dict(`regex`={regex}, `type_dict`={type_dict}, `default`='{default}', debug={debug}) was called")

        # If the `regex` is a string, compile so we can access match group info
        if isinstance(regex, str):
            regex = re.compile(regex)

        if isinstance(regex, re.Match) and isinstance(type_dict, dict):
            # If the `regex` matches, cast the results as the values
            # in `type_dict`...
            _groupdict = regex.groupdict()
            for _regex_key, _type in type_dict.items():
                retval[_regex_key] = _groupdict.get(_regex_key, default)
                if _type is not None and retval[_regex_key] != default:
                    retval[_regex_key] = _type(retval[_regex_key])
        elif regex is None and isinstance(type_dict, dict):
            # If the regex did not match, None is returned... and we should
            # assign the default to the regex key...
            for _regex_key in type_dict.keys():
                retval[_regex_key] = default
        else:
            error = f"`regex` must be the result of a regex match, and `type_dict` must be a dict of types; however we received `regex`: {type(regex)} and `type_dict`: {type(type_dict)}."
            logger.critical(error)
            raise InvalidTypecast(error)
        return retval

    # On BaseCfgLine()
    def re_sub(self, regex, replacergx, ignore_rgx=None):
        """Replace all strings matching ``linespec`` with ``replacestr`` in the :class:`~models_cisco.IOSCfgLine` object; however, if the :class:`~models_cisco.IOSCfgLine` text matches ``ignore_rgx``, then the text is *not* replaced.
        Parameters
        ----------
        regex : str
            A string or python regular expression, which should be matched.
        replacergx : str
            A string or python regular expression, which should replace the text matched by ``regex``.
        ignore_rgx : str
            A string or python regular expression; the replacement is skipped if :class:`~models_cisco.IOSCfgLine` text matches ``ignore_rgx``.  ``ignore_rgx`` defaults to None, which means no lines matching ``regex`` are skipped.

        Returns
        -------
        str
            The new text after replacement

        Examples
        --------
        This example illustrates how you can use
        :func:`~models_cisco.IOSCfgLine.re_sub` to replace ``Serial1`` with
        ``Serial0`` in a configuration...
        .. code-block:: python
           :emphasize-lines: 15
           >>> from ciscoconfparse import CiscoConfParse
           >>> config = [
           ...     '!',
           ...     'interface Serial1/0',
           ...     ' ip address 1.1.1.1 255.255.255.252',
           ...     '!',
           ...     'interface Serial1/1',
           ...     ' ip address 1.1.1.5 255.255.255.252',
           ...     '!',
           ...     ]
           >>> parse = CiscoConfParse(config)
           >>>
           >>> for obj in parse.find_objects('Serial'):
           ...     print("OLD {}".format(obj.text))
           ...     obj.re_sub(r'Serial1', r'Serial0')
           ...     print("  NEW {}".format(obj.text))
           OLD interface Serial1/0
             NEW interface Serial0/0
           OLD interface Serial1/1
             NEW interface Serial0/1
           >>>
        """
        # When replacing objects, check whether they should be deleted, or
        #   whether they are a comment
        if ignore_rgx and re.search(ignore_rgx, self._text):
            return self._text

        retval = re.sub(regex, replacergx, self._text)

        # Delete empty lines
        if retval.strip() == "":
            self.delete()
            return

        self._text = retval
        self.set_comment_bool()
        return retval

    # On BaseCfgLine()
    def re_match(self, regex, group=1, default=""):
        r"""Use ``regex`` to search the :class:`~models_cisco.IOSCfgLine` text and return the regular expression group, at the integer index.
        Parameters
        ----------
        regex : str
            A string or python regular expression, which should be matched.  This regular expression should contain parenthesis, which bound a match group.
        group : int
            An integer which specifies the desired regex group to be returned.  ``group`` defaults to 1.
        default : str
            The default value to be returned, if there is no match.  By default an empty string is returned if there is no match.
        Returns
        -------
        str
            The text matched by the regular expression group; if there is no match, ``default`` is returned.
        Examples
        --------
        This example illustrates how you can use
        :func:`~models_cisco.IOSCfgLine..re_match` to store the mask of the
        interface which owns "1.1.1.5" in a variable called ``netmask``.
        .. code-block:: python
           :emphasize-lines: 14
           >>> from ciscoconfparse import CiscoConfParse
           >>> config = [
           ...     '!',
           ...     'interface Serial1/0',
           ...     ' ip address 1.1.1.1 255.255.255.252',
           ...     '!',
           ...     'interface Serial1/1',
           ...     ' ip address 1.1.1.5 255.255.255.252',
           ...     '!',
           ...     ]
           >>> parse = CiscoConfParse(config)
           >>>
           >>> for obj in parse.find_objects(r'ip\saddress'):
           ...     netmask = obj.re_match(r'1\.1\.1\.5\s(\S+)')
           >>>
           >>> print("The netmask is", netmask)
           The netmask is 255.255.255.252
           >>>
        """
        mm = re.search(regex, self.text)
        if mm is not None:
            return mm.group(group)
        return default

    # On BaseCfgLine()
    def re_search(self, regex, default="", debug=0):
        """Search :class:`~models_cisco.IOSCfgLine` with ``regex``

        Parameters
        ----------
        regex : str
            A string or python regular expression, which should be matched.
        default : str
            A value which is returned if :func:`~ccp_abc.re_search()` doesn't find a match while looking for ``regex``.
        Returns
        -------
        str
            The :class:`~models_cisco.IOSCfgLine` text which matched.  If there is no match, ``default`` is returned.
        """
        # assert isinstance(default, str)
        # assert isinstance(debug, int)

        retval = default
        # Shortcut with a substring match, if possible...
        if isinstance(regex, str) and (regex in self.text):
            if debug > 0:
                logger.debug("'{}' is a substring of '{}'".format(regex, self.text))
            retval = self.text
        elif re.search(regex, self.text) is not None:
            ## TODO: use re.escape(regex) on all regex, instead of bare regex
            if debug > 0:
                logger.debug("re.search('{}', '{}') matches".format(regex, self.text))
            retval = self.text
        return retval

    # On BaseCfgLine()
    def re_search_children(self, regex, recurse=False):
        """Use ``regex`` to search the text contained in the children of
        this :class:`~models_cisco.IOSCfgLine`.
        Parameters
        ----------
        regex : str
            A string or python regular expression, which should be matched.
        recurse : bool
            Set True if you want to search all children (children, grand children, great grand children, etc...)
        Returns
        -------
        list
            A list of matching :class:`~models_cisco.IOSCfgLine` objects which matched.  If there is no match, an empty :py:func:`list` is returned.
        """
        if recurse is False:
            return [cobj for cobj in self.children if cobj.re_search(regex)]
        else:
            return [cobj for cobj in self.all_children if cobj.re_search(regex)]

    # On BaseCfgLine()
    def re_match_typed(
        self, regex, group=1, untyped_default=False, result_type=str, default=""
    ):
        r"""Use ``regex`` to search the :class:`~models_cisco.IOSCfgLine` text
        and return the contents of the regular expression group, at the
        integer ``group`` index, cast as ``result_type``; if there is no match,
        ``default`` is returned.
        Parameters
        ----------
        regex : str
            A string or python regular expression, which should be matched.  This regular expression should contain parenthesis, which bound a match group.
        group : int
            An integer which specifies the desired regex group to be returned.  ``group`` defaults to 1.
        result_type : type
            A type (typically one of: ``str``, ``int``, ``float``, or ``IPv4Obj``).  All returned values are cast as ``result_type``, which defaults to ``str``.
        default : any
            The default value to be returned, if there is no match.
        untyped_default : bool
            Set True if you don't want the default value to be typed
        Returns
        -------
        ``result_type``
            The text matched by the regular expression group; if there is no match, ``default`` is returned.  All values are cast as ``result_type``, unless `untyped_default` is True.
        Examples
        --------
        This example illustrates how you can use
        :func:`~models_cisco.IOSCfgLine.re_match_typed` to build an
        association between an interface name, and its numerical slot value.
        The name will be cast as :py:func:`str`, and the slot will be cast as
        :py:func:`int`.
        .. code-block:: python
           :emphasize-lines: 15,16,17,18,19
           >>> from ciscoconfparse import CiscoConfParse
           >>> config = [
           ...     '!',
           ...     'interface Serial1/0',
           ...     ' ip address 1.1.1.1 255.255.255.252',
           ...     '!',
           ...     'interface Serial2/0',
           ...     ' ip address 1.1.1.5 255.255.255.252',
           ...     '!',
           ...     ]
           >>> parse = CiscoConfParse(config)
           >>>
           >>> slots = dict()
           >>> for obj in parse.find_objects(r'^interface'):
           ...     name = obj.re_match_typed(regex=r'^interface\s(\S+)',
           ...         default='UNKNOWN')
           ...     slot = obj.re_match_typed(regex=r'Serial(\d+)',
           ...         result_type=int,
           ...         default=-1)
           ...     print("Interface {0} is in slot {1}".format(name, slot))
           ...
           Interface Serial1/0 is in slot 1
           Interface Serial2/0 is in slot 2
           >>>
        """
        mm = re.search(regex, self.text)
        if mm is not None:
            if mm.group(group) is not None:
                return result_type(mm.group(group))
        if untyped_default:
            return default
        else:
            return result_type(default)

    # On BaseCfgLine()
    @logger.catch(reraise=True)
    def re_match_iter_typed(
        self,
        regex,
        group=1,
        result_type=str,
        default="",
        untyped_default=False,
        groupdict=None,
        recurse=True,
        debug=False,
    ):
        r"""Use ``regex`` to search the children of
        :class:`~models_cisco.IOSCfgLine` text and return the contents of
        the regular expression group, at the integer ``group`` index, cast as
        ``result_type``; if there is no match, ``default`` is returned.
        Parameters
        ----------
        regex : str
            A string or python compiled regular expression, which should be matched.  This regular expression should contain parenthesis, which bound a match group.
        group : int
            An integer which specifies the desired regex group to be returned.  ``group`` defaults to 1; this is only used if ``groupdict`` is None.
        result_type : type
            A type (typically one of: ``str``, ``int``, ``float``, or :class:`~ccp_util.IPv4Obj`).  All returned values are cast as ``result_type``, which defaults to ``str``.  This is only used if ``groupdict`` is None.
        default : any
            The default value to be returned, if there is no match.
        recurse : bool
            Set True if you want to search all children (children, grand children, great grand children, etc...)
        untyped_default : bool
            Set True if you don't want the default value to be typed; this is only used if ``groupdict`` is None.
        groupdict : dict
            Set to a dict of types if you want to match on regex group names; ``groupdict`` overrides the ``group``, ``result_type`` and ``untyped_default`` arguments.
        debug : bool
            Set True if you want to debug ``re_match_iter_typed()`` activity

        Returns
        -------
        ``result_type``
            The text matched by the regular expression group; if there is no match, ``default`` is returned.  All values are cast as ``result_type``, unless `untyped_default` is True.
        Notes
        -----
        This loops through the children (in order) and returns when the regex hits its first match.

        Examples
        --------
        This example illustrates how you can use
        :func:`~models_cisco.IOSCfgLine.re_match_iter_typed` to build an
        :func:`~ccp_util.IPv4Obj` address object for each interface.
           >>> import re
           >>> from ciscoconfparse import CiscoConfParse
           >>> from ciscoconfparse.ccp_util import IPv4Obj
           >>> config = [
           ...     '!',
           ...     'interface Serial1/0',
           ...     ' ip address 1.1.1.1 255.255.255.252',
           ...     '!',
           ...     'interface Serial2/0',
           ...     ' ip address 1.1.1.5 255.255.255.252',
           ...     '!',
           ...     ]
           >>> parse = CiscoConfParse(config)
           >>> INTF_RE = re.compile(r'interface\s\S+')
           >>> ADDR_RE = re.compile(r'ip\saddress\s(\S+\s+\S+)')
           >>> for obj in parse.find_objects(INTF_RE):
           ...     print("{} {}".format(obj.text, obj.re_match_iter_typed(ADDR_RE, result_type=IPv4Obj)))
           interface Serial1/0 <IPv4Obj 1.1.1.1/30>
           interface Serial2/0 <IPv4Obj 1.1.1.5/30>
           >>>
        """
        ## iterate through children, and return the matching value
        ##  (cast as result_type) from the first child.text that matches regex
        # if (default is True):
        ## Not using self.re_match_iter_typed(default=True), because I want
        ##   to be sure I build the correct API for match=False
        ##
        ## Ref IOSIntfLine.has_dtp for an example of how to code around
        ##   this while I build the API
        #    raise NotImplementedError
        if debug is True:
            logger.info(f"{self}.re_match_iter_typed(`regex`={regex}, `group`={group}, `result_type`={result_type}, `recurse`={recurse}, `untyped_default`={untyped_default}, `default`='{default}', `groupdict`={groupdict}, `debug`={debug}) was called")

        if groupdict is None:
            if debug is True:
                logger.debug(f"    {self}.re_match_iter_typed() is checking with `groupdict`=None")

            # Return the result if the parent line matches the regex...
            mm = re.search(regex, self.text)
            if isinstance(mm, re.Match):
                return result_type(mm.group(group))

            if recurse is False:
                for cobj in self.children:
                    if debug is True:
                        logger.debug(f"    {self}.re_match_iter_typed() is checking match of r'''{regex}''' on -->{cobj}<--")
                    mm = re.search(regex, cobj.text)
                    if isinstance(mm, re.Match):
                        return result_type(mm.group(group))
                ## Ref Github issue #121
                if untyped_default is True:
                    return default
                else:
                    return result_type(default)
            else:
                for cobj in self.all_children:
                    if debug is True:
                        logger.debug(f"    {self}.re_match_iter_typed() is checking match of r'''{regex}''' on -->{cobj}<--")
                    mm = re.search(regex, cobj.text)
                    if isinstance(mm, re.Match):
                        return result_type(mm.group(group))
                ## Ref Github issue #121
                if untyped_default is True:
                    return default
                else:
                    return result_type(default)
        elif isinstance(groupdict, dict) is True:
            if debug is True:
                logger.debug(f"    {self}.re_match_iter_typed() is checking with `groupdict`={groupdict}")

            # Return the result if the parent line matches the regex...
            mm = re.search(regex, self.text)
            if isinstance(mm, re.Match):
                return self.get_typed_dict(
                    regex=mm,
                    type_dict=groupdict,
                    default=default,
                    debug=debug,
                )

            if recurse is False:
                for cobj in self.children:
                    mm = re.search(regex, cobj.text)
                    return self.get_typed_dict(
                        regex=mm,
                        type_dict=groupdict,
                        default=default,
                        debug=debug,
                    )
                return self.get_typed_dict(
                    regex=mm,
                    type_dict=groupdict,
                    default=default,
                    debug=debug,
                )
            else:
                for cobj in self.all_children:
                    mm = re.search(regex, cobj.text)
                    if isinstance(mm, re.Match):
                        return self.get_typed_dict(
                            regex=mm,
                            type_dict=groupdict,
                            default=default,
                            debug=debug,
                        )
                return self.get_typed_dict(
                    regex=mm,
                    type_dict=groupdict,
                    default=default,
                    debug=debug,
                )
        else:
            error = f"`groupdict` must be None or a `dict`, but we got {type(groupdict)}."
            logger.error(error)
            raise ValueError(error)

    # On BaseCfgLine()
    def reset(self):
        # For subclass APIs
        raise NotImplementedError

    # On BaseCfgLine()
    def build_reset_string(self):
        # For subclass APIs
        raise NotImplementedError

    # On BaseCfgLine()
    @property
    def ioscfg(self):
        """Return a list with this the text of this object, and
        with all children in the direct line."""
        retval = [self.text]
        retval.extend([ii.text for ii in self.all_children])
        return retval

    # On BaseCfgLine()
    @property
    def lineage(self):
        """Iterate through to the oldest ancestor of this object, and return
        a list of all ancestors / children in the direct line.  Cousins or
        aunts / uncles are *not* returned.  Note: all children of this
        object are returned."""
        retval = self.all_parents
        retval.append(self)
        if self.children:
            retval.extend(self.all_children)
        return sorted(retval)

    # On BaseCfgLine()
    @property
    def geneology(self):
        """Iterate through to the oldest ancestor of this object, and return
        a list of all ancestors' objects in the direct line as well as this
        obj.  Cousins or aunts / uncles are *not* returned.  Note: children
        of this object are *not* returned."""
        retval = sorted(self.all_parents)
        retval.append(self)
        return retval

    # On BaseCfgLine()
    @property
    def geneology_text(self):
        """Iterate through to the oldest ancestor of this object, and return
        a list of all ancestors' .text field for all ancestors in the direct
        line as well as this obj.  Cousins or aunts / uncles are *not*
        returned.  Note: children of this object are *not* returned."""
        retval = [ii.text for ii in self.geneology]
        return retval

    # On BaseCfgLine()
    @property
    def is_parent(self):
        return bool(self.has_children)

    # On BaseCfgLine()
    @property
    def is_child(self):
        return not bool(self.parent == self)

    # On BaseCfgLine()
    @property
    def siblings(self):
        indent = self.indent
        return [obj for obj in self.parent.children if (obj.indent == indent)]

    # On BaseCfgLine()
    @classmethod
    def is_object_for(cls, line=""):
        return False
