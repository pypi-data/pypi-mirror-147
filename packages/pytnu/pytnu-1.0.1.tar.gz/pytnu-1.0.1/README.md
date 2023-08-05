# pytnu
An easy interface to create text-menus with
  
## About The Project

pytnu is a lightweight, easy to use menu creation interface that allows you to create easy text-based menus. It supports nested menus and allows the user to easily build a user interface;


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This package uses no prerequisites and no external packages are necessary.

### Installation

1. Install the package using pip
   ```sh
   pip install pytnu
<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage
![enter image description here](https://i.imgur.com/U239Xai.png)

 1. Import pytnu 
 2. Create a dictionary with your options and descriptions
`options = {name: (description, functionName)}`
Name is the keyword the user inputs to call the option
Description is the text that tells the user what the option does
functionName is the name of the function to be called, without the parenthesis.

 4. Create a Menu object using `Menu(options)`
 5. To start the menu, use `Menu.start()`

To re-create the menu seen above:

    options = {"opt1": ("Prints Foo", printFoo), "opt2": ("Prints Bar", printBar)}
    menu = Menu(options)
    menu.start()
<p align="right">(<a href="#top">back to top</a>)</p>

## Methods

 

    Menu.addOption(name, description, funcName)
Adds an option to the available options of a menu class

    Menu.delOption(name)
  Deletes an option based on the given name 

<p align="right">(<a href="#top">back to top</a>)</p>






