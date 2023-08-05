# uzoenr Text Browser

uzoenr is an unique text web browser: it can open FB2 books. :flushed:

## license

````
Uzoenr - text web browser
Copyright (C) 2022 Tabaqui
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
````

## Using
````
uzoenr
````

````
#USING IN IDLE/GEANY
from uzoenr.uzoenr import start
start()
````

### Embedding

````
from uzoenr.uzoenr import Engine
...
parser = Engine()
parser.feed(data)
return parser.data()
````

## Commands:

**DISCLAIMER: FORMS MAY NOT WORK IF SITE USES JAVASCRIPT!**

* `l url` - load a new url (writing **WITHOUT** space)
* `num num` (num is an integer) - show a part of document (first number must be less then second)
* `num` - show a part beginning from line number <num>
* `d<url> <filename>` (url - URL; filename - path for saving) - download file (DO NOT USE SPACE BEFORE URL BUT USE IT BETWEEN PARAMETERS)
* `q` - close the browser
* `B<bm>` - load a bookmark (write without spaces)
* `b<bm> <url>` - add a bookmark (bookmark name **MUST** be written without space)
* `F<name> <data>` - input data to form
* `f<url>` - load the page with the form (url **MUST** be written without space)
* `H<url>` - set homepage to URL url (DO **NOT** ENTER SPACES)
* `R<file>` - open FB2 book (DO **NOT** ENTER SPACES AFTER R LETTER)
* `s<data>` - find data in page (DO **NOT** ENTER SPACES AFTER s LETTER!)
* `p<name> <value>` - create a point named <name> with line <value> (<value> is INT)
* `P<name>` - open line with <name> in current page
* `!<name>` - open the page associated with name at the point with the same name)
