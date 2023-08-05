from ipyvue import VueWidget
import ipyvuetify as v
from traitlets import Unicode, Bool, observe

__all__ = ["SepalWidget"]


class SepalWidget(v.VuetifyWidget):
    """
    Custom vuetifyWidget to add specific methods
    """

    viz = Bool(True).tag(sync=True)
    "Bool: whether the widget is displayed or not"

    old_class = Unicode("").tag(sync=True)
    "Unicode: a saving attribute of the widget class"

    def __init__(self, **kwargs):

        # remove viz from kwargs
        # class_list need to be setup before viz
        # to let hide and shw function run
        viz = kwargs.pop("viz", True)

        # init the widget
        super().__init__(**kwargs)

        # setup the viz status
        self.viz = viz

    @observe("viz")
    def _set_viz(self, change):
        """
        hide or show the component according to its viz param value.

        Hide the widget by reducing the html class to :code:`d-none`.
        Show the widget by removing the :code:`d-none` html class.
        Save the previous class

        Args:
            change: the dict of a trait callback
        """

        # will be replaced byt direct calls to built-in hide
        # once the previous custom implementation will be fully removed

        if self.viz:

            # change class value
            self.class_ = self.old_class or self.class_
            self.class_list.remove("d-none")

        else:

            # change class value
            self.class_list.remove("d-none")
            self.old_class = str(self.class_)
            self.class_ = "d-none"

        return

    def toggle_viz(self):
        """
        toogle the visibility of the widget.

        Return:
            self
        """

        self.viz = not self.viz

        return self

    def hide(self):
        """
        Hide the widget by reducing the html class to :code:`d-none`.
        Save the previous class and set viz attribute to False.

        Return:
            self
        """

        # update viz state
        self.viz = False

        return self

    def show(self):
        """
        Show the widget by removing the d-none html class.
        Save the previous class and set viz attribute to True.

        Return:
            self
        """

        # update viz state
        self.viz = True

        return self

    def reset(self):
        """
        Clear the widget v_model. Need to be extented in custom widgets to fit the structure of the actual input.

        Return:
            self
        """

        self.v_model = None

        return self

    def get_children(self, id_):
        """Retrieve all children elements that matches with the given id_.

        Args:
            id_ (str, optional): attribute id to compare with.

        Returns:
            Will return a list with all mathing elements if there are more than one,
            otherwise will return the mathing element.

        """

        elements = []

        def search_children(parent):

            if issubclass(parent.__class__, VueWidget):

                if parent.attributes.get("id") == id_:
                    elements.append(parent)

                if len(parent.children):
                    [search_children(chld) for chld in parent.children]

        # Search in the self children elements
        [search_children(chld) for chld in self.children]

        return elements[0] if len(elements) == 1 else elements

    def set_children(self, children, position="first"):
        """Insert input children in self children within given position

        Args:
            children (str, DOMWidget, list(str, DOMWidget)):
            position (str): whether to insert as first or last element. ["first", "last"]
        """

        if not isinstance(children, list):
            children = [children]

        new_childrens = self.children[:]

        if position == "first":
            new_childrens = children + new_childrens

        elif position == "last":
            new_childrens = new_childrens + children

        else:
            raise ValueError(
                f"Position '{position}' is not a valid value. Use 'first' or 'last'"
            )

        self.children = new_childrens

        return self
