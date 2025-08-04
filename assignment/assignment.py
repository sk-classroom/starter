import marimo

__generated_with = "0.14.13"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ![](https://www.bleepstatic.com/content/hl-images/2022/04/08/GitHub__headpic.jpg)

    # Interactive Data Visualization with marimo

    Welcome to your first interactive data visualization assignment! You'll learn plotting and data exploration through hands-on experimentation with marimo's reactive notebook interface.

    # 📚 Understanding marimo Notebooks

    Before diving into data visualization, let's explore marimo's unique features that make interactive computing powerful and intuitive.
    """
    )
    return


@app.cell
def _():
    # All imports in one place to avoid conflicts
    import numpy as np
    import matplotlib.pyplot as plt

    return np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 🔑 Key Concept 1: Reactive Programming

    In marimo, when you change one thing, everything that depends on it updates automatically! No need to manually re-run cells.

    Let's see this in action with a simple example:
    """
    )
    return


@app.cell
def _(mo):
    # Try changing this slider and watch what happens below!
    demo_slider = mo.ui.slider(start=1, stop=10, value=5, label="🎯 Change me!")
    demo_slider
    return (demo_slider,)


@app.cell
def _(demo_slider):
    # This cell automatically updates when you move the slider above!
    squared_value = demo_slider.value ** 2
    f"The square of {demo_slider.value} is {squared_value}"
    return (squared_value,)


@app.cell
def _(demo_slider, plt, squared_value):
    # This plot also updates automatically!
    _fig, _ax = plt.subplots(figsize=(6, 4))
    _ax.bar(['Original', 'Squared'], [demo_slider.value, squared_value],
           color=['lightblue', 'lightcoral'])
    _ax.set_title('Reactive Updates in Action!')
    _ax.set_ylabel('Value')
    plt.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **🎉 Did you see that?** When you moved the slider:
    1. The text updated automatically
    2. The plot redrawed automatically
    3. No manual clicking "Run" buttons!

    This is **reactive programming** - the core magic of marimo!

    ## 🔑 Key Concept 2: Variable Scoping

    In marimo's visual interface, you don't see function definitions, but behind the scenes, each cell is a function. Variables are shared between cells automatically.

    /// attention | Attention!
    Each variable name can only be defined in one cell. If you try to define the same variable in multiple cells, marimo will show you an error.
    ///


    - ✅ **Good**: Each cell defines unique variables

    - ❌ **Bad**: Multiple cells defining `data = ...`

    **🔧 Pro Tip**: Use underscore prefix for local variables that don't need to be shared:
    - `_fig, _ax = plt.subplots()` instead of `fig, ax = plt.subplots()`
    - `_temp_data = process(data)` for temporary calculations
    - `_i, _j, _k` for loop counters

    This prevents conflicts when multiple cells create plots or temporary variables!

    Example:

    - The following cell causes an error because it redefines the same variable `sample_data` in multiple cells.

    - To resolve this, you need to rename the variable name in the either cell to something else. If the variable is used only in that cell, you can use an underscore prefix, i.e., `_sample_data = ...`.
    """
    )
    return

@app.cell
def _(mo, np):
    sample_data = np.array([1,2,3,4,5])
    return

@app.cell
def _(mo, sample_data):
    _sample_data = sample_data ** 2
    f"The square of the sample data is {_sample_data}"
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 🔑 Key Concept 3: Order Doesn't Matter

    In traditional notebooks, cell order matters. In marimo, it doesn't! marimo automatically figures out the right execution order based on dependencies.

    **🧪 Interactive Example**: Try this - the cells below are intentionally in "wrong" order in traditional sense, but they work perfectly! This is particularly useful when you want to bring your visualization up front and then all the data loading and processing later.
    """
    )
    return


@app.cell
def _(mo, demo_slider_number):
    # Cell B: This processes the data (but comes in middle!)
    final_message = "👉: " + "🐛" * demo_slider_number.value
    mo.md(final_message)
    return (final_message,)


@app.cell
def _(mo):
    # Cell A: This creates the initial data (but comes last!)
    # Change this number and see if the number above changes
    demo_slider_number = mo.ui.slider(start=1, stop=10, value=1, label="🎯 Change me!")
    demo_slider_number
    return (demo_slider_number,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **🤯 Did you see that?** Even though the cells are in order C → B → A, marimo automatically ran them as A → B → C based on dependencies!
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**Notice**: The imports are defined at the top of the notebook, but marimo's dependency system means you can use them anywhere - even in cells that appear "before" the imports!""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **🎯 Ready for the Assignment?**

    I hope that I prepared you well for the assignment based on marimo notebook.

    Let's dive into the assignment!

    ---

    # 📋 Assignment Instructions & Grading
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "📋 Assignment Tasks": mo.md(
            r"""
            Complete the following tasks and upload your notebook to your GitHub repository.

            1. Fill in the blank functions, marked by "\#TODO", in the notebook
            2. Update this notebook by using `git add`, `git commit`, and then `git push`.
            3. The notebook will be automatically graded, and your score will be shown on GitHub. See [how to check the results on GitHub](https://docs.github.com/en/education/manage-coursework-with-github-classroom/learn-with-github-classroom/view-autograding-results)
            """
        ),
        "🔒 Protected Files": mo.md(
            r"""
            Protected files are test files and configuration files you cannot modify. They appear in your repository but don't make any changes to them. You can change them and commit them to your repository, but any changes you make to them will be notified to the instructor for review.
            """
        ),
        "⚖️ Academic Integrity": mo.md(
            r"""
            There is a system that automatically checks code similarity across all submissions and online repositories. Sharing code or submitting copied work will result in zero credit and disciplinary action.

            While you can discuss concepts, each student must write their own code. Cite any external resources, including AI tools, in your comments. Start early and ask for help during office hours if needed. The goal is to learn through genuine effort, not shortcuts.
            """
        ),
        "📚 Allowed Libraries": mo.md(
            r"""
            You **cannot** import any other libraries that result in the grading script failing or a zero score. So make sure NOT to import any other libraries!
            """
        )
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 1

    Let us learn how the grading works through the following example.
    First, there two types of cells, i.e., those that are graded and those that are not.
    We will evaluate only the cells that are marked as "\#Task".
    For almost all cases, the task is to implement a Python function.
    The Python function is accompanied by the docstring that specifies the input and output of the function.
    Your task is to implement the function and test it.

    Example:
    ```python
    #Task
    def calc_square(x):
        '''
        Calculate the square of a number.

        Args:
            x (int): The number to square.

        Returns:
            int: The square of the number.
        '''
        )
        pass
        return
    ```

    /// attention | Attention!
    Do not import any libraries inside the function. This will cause the grading to fail.
    ///

    Once you implement the function, you can test it by running the cell.
    The test will be automatically graded and the result will be shown on GitHub.

    To demonstrate how the grading works, let's implement the function.
    """
    )

@app.function
def calc_square(x):
    """
    #TASK: Implement the function

    Input:
        x: numpy array
    Output:
        numpy array. The square of the input.
    """
    return x

@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Once done, git commit & push the notebook to your GitHub repository. You can do this using the Web interface.
    See [how to upload your assingment](https://docs.google.com/presentation/d/19Zvrp5kha6ohF4KvTX9W2jodKkfmsOrJfEZtO_Wg0go)


    The notebook will be automatically graded via GitHub Actions. You can check the results on GitHub. See [how to check the grading results on GitHub](https://docs.google.com/presentation/d/19Zvrp5kha6ohF4KvTX9W2jodKkfmsOrJfEZtO_Wg0go/edit?usp=sharing)

    """
    )

@app.cell
def _():
    import marimo as mo
    return (mo,)

if __name__ == "__main__":
    app.run()
