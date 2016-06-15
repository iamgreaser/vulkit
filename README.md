vulkit - currently just a wrapper generator for Vulkan 

Basically, libepoxy, but for Vulkan.

## Requirements

* A suitable Vulkan SDK with headers
* Python - 2 or 3, doesn't matter, it does work with 2.7 and 3.4

## Installation

    ./build.sh
    ./install.sh

Or if you wish to install it to a different prefix:

    ./build.sh
    PREFIX=/usr ./install.sh

## Usage

1. Include `<vulkit/vulkan.h>` instead of `<vulkan/vulkan.h>`.
2. Link with `-lvulkit`.
3. ???
4. ...TRIANGLE!

At the time of writing I am still working on step 3.

Note, you will still have to use `vkCreateInstance` yourself, and THIS
MUST BE THE FIRST THING YOU CALL. Furthermore, you MUST use lazy
binding, as the other wrapper functions depend on you calling
`vkCreateInstance` and stealing the instance handle from that call.

