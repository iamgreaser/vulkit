"""
vulkit wrapper generator
Copyright (c) 2016, Ben Russell

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import xml.etree.ElementTree as ET

def ensure(cond):
	assert cond

fp_header = open("vulkan.h", "w")
fp_source = open("vulkit_wrapper.c", "w")

tree = ET.parse("vk.xml")
commands = []
extensions = {}
cmd_ext_map = {}
root = tree.getroot()
ensure(root.tag == "registry")

def output_to_header(s):
	fp_header.write(s + "\n")

def output_to_source(s):
	fp_source.write(s + "\n")

def gen_param_prototype(ptype, name):
	s = "%s %s" % (ptype, name, )
	return s

def gen_command_prototype(rtype, name, params):
	s = "%s vulkit_proto_%s (%s);" % (rtype, name, ', '.join(gen_param_prototype(*p) for p in params), )
	if name in cmd_ext_map:
		s = "#ifdef %s\n%s\n#endif" % (cmd_ext_map[name], s, )
	output_to_header(s)

def gen_command_map(rtype, name, params):
	s = "#define %s vulkit_proto_%s" % (name, name, )
	output_to_header(s)

def gen_command_ifunc(rtype, name, params):
	proto = ', '.join(gen_param_prototype(*p) for p in params)

	if name == "vkCreateInstance":
		proto2 = ', '.join(p[1] for p in params[:])
		s = (
"""%s vulkit_proto_%s (%s)
{
	PFN_%s create_inst = (PFN_%s)vkGetInstanceProcAddr(NULL, "%s");
	VkResult res = create_inst(%s);
	memcpy(&vulkit_last_instance, %s, sizeof(VkInstance));
	return res;
}
""" ) % (
			rtype, name, proto,

			name, name, name,
			proto2,
			params[-1][1], 
		)

	else:
		s = (
"""static PFN_%s resolve_%s(void)
{
	return (PFN_%s)vkGetInstanceProcAddr(vulkit_last_instance, "%s");
}

%s vulkit_proto_%s (%s) __attribute__((ifunc ("resolve_%s")));
""") % (
			name, name,

			name, name,

			rtype, name, proto, name,
		)
		
	if name in cmd_ext_map:
		s = "#ifdef %s\n%s#endif\n" % (cmd_ext_map[name], s, )
	output_to_source(s)

for c0 in root:
	if c0.tag == "extensions":
		for extension in c0:
			ensure(extension.tag == "extension")
			ext_name = extension.attrib["name"]
			ensure(ext_name)
			#print((extension.tag, extension.attrib))
			for c1 in extension:
				ensure(c1.tag == "require")
				for c2 in c1:
					if c2.tag == "enum":
						pass
					elif c2.tag == "type":
						pass
					elif c2.tag == "command":
						#print((c2.attrib))
						cmd_name = c2.attrib["name"]
						ensure(cmd_name)
						cmd_ext_map[cmd_name] = ext_name
					elif c2.tag == "usage":
						pass
					else:
						print(repr(c2.tag))
						ensure(False)

	elif c0.tag == "commands":
		for command in c0:
			ensure(command.tag == "command")

			cmd_type = None
			cmd_name = None
			cmd_params = []

			for c1 in command:
				if c1.tag == "proto":
					ensure(cmd_name == None)
					ensure(cmd_type == None)

					cmd_type_prefix = c1.text
					cmd_type_suffix = None

					for c2 in c1:
						if c2.tag == "type":
							cmd_type = c2.text
							cmd_type_suffix = c2.tail
						elif c2.tag == "name":
							cmd_name = c2.text
						else:
							assert(False)

					ensure(cmd_name != None)
					ensure(cmd_type != None)

					if cmd_type_prefix == None:
						pass
					elif cmd_type_prefix in ["const "]:
						cmd_type = cmd_type_prefix + cmd_type
					else:
						print(repr(cmd_type_prefix))
						ensure(False)

					if cmd_type_suffix == None:
						pass
					elif cmd_type_suffix in ["* ", "** "]:
						cmd_type += " " + cmd_type_suffix[:-1]
					elif cmd_type_suffix in [" "]:
						pass
					else:
						print(repr(cmd_type_suffix))
						ensure(False)

				elif c1.tag == "param":
					p_type = None
					p_name = None

					p_type_prefix = c1.text
					p_type_suffix = None

					for c2 in c1:
						if c2.tag == "type":
							p_type = c2.text
							p_type_suffix = c2.tail
						elif c2.tag == "name":
							p_name = c2.text
						else:
							assert(False)

					ensure(p_name != None)
					ensure(p_type != None)

					if p_type_prefix == None:
						pass
					elif p_type_prefix in ["const ", "struct "]:
						p_type = p_type_prefix + p_type
					else:
						print(repr(p_type_prefix))
						ensure(False)

					if p_type_suffix == None:
						pass
					elif p_type_suffix in ["* ", "** "]:
						p_type += " " + p_type_suffix[:-1]
					elif p_type_suffix in [" "]:
						pass
					else:
						print(repr(p_type_suffix))
						ensure(False)

					cmd_params.append((p_type, p_name))

				elif c1.tag == "validity":
					pass

				elif c1.tag == "implicitexternsyncparams":
					pass

				else:
					print(c1.tag)
					ensure(False)

			commands.append((cmd_type, cmd_name, cmd_params))

def tap_commands(proto_tap):
	for c in commands:
		proto_tap(*c)
	

output_to_header(
"""#ifndef VULKIT_VULKAN_H_
#define VULKIT_VULKAN_H_ 1
#ifdef VULKAN_H_
#error "Don't include vulkan/vulkan.h, just include vulkit/vulkan.h"
#else
#include <vulkan/vulkan.h>
#endif
""")
tap_commands(gen_command_prototype)
output_to_header("")
tap_commands(gen_command_map)
output_to_header("")
output_to_header(
"""#endif
""")

output_to_source(
"""#include <string.h>

#define VK_KHR_surface 1
#include <vulkan/vulkan.h>

static VkInstance vulkit_last_instance = VK_NULL_HANDLE;
""")
tap_commands(gen_command_ifunc)
output_to_source("")

