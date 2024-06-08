#!/usr/bin/python3
""" Console Module """
import cmd
import sys
import re
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review


def handle_update(args):
    regex = r"(.+?),\s*(.+?),\s*(.+?)"
    match = re.match(regex, args)
    if match:
        obj_id = match.group(1)
        name = match.group(2)
        value = match.group(3)
        return f"{obj_id} {name} {value}"
    return args


def parse_value(value):
    """parse the value string and return the value based on the type"""
    if value[0] == '"' and value[-1] == '"':
        value = value[1: -1]
        value = value.replace('\\"', '"')
        value = value.replace('_', ' ')
        return value
    elif re.match(r"^-?\d+\.\d+$", value) or value == 'inf' or value == 'NaN':
        return float(value)
    # Useless commemnt to test something
    elif value.isdigit() or value[1:].isdigit():
        return int(value)
    else:
        return None


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def onecmd(self, line):
        """Redefine the oncmd function"""
        regex = r"^(.+)\.(\w+)\((.*)\)"

        result = re.match(regex, line)
        if result:
            model = result.group(1)
            command = result.group(2)
            args = result.group(3)
            if command == "update":
                args = handle_update(args)
            line = f"{command} {model} {args}"
        super().onecmd(line)

    # def precmd(self, line):
    #     """Reformat command line for advanced command syntax.

    #     Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
    #     (Brackets denote optional fields in usage example.)
    #     """
    #     _cmd = _cls = _id = _args = ''  # initialize line elements

    #     # scan for general formating - i.e '.', '(', ')'
    #     if not ('.' in line and '(' in line and ')' in line):
    #         return line

    #     try:  # parse line left to right
    #         pline = line[:]  # parsed line

    #         # isolate <class name>
    #         _cls = pline[:pline.find('.')]

    #         # isolate and validate <command>
    #         _cmd = pline[pline.find('.') + 1:pline.find('(')]
    #         if _cmd not in HBNBCommand.dot_cmds:
    #             raise Exception

    #         # if parantheses contain arguments, parse them
    #         pline = pline[pline.find('(') + 1:pline.find(')')]
    #         if pline:
    #             # partition args: (<id>, [<delim>], [<*args>])
    #             pline = pline.partition(', ')  # pline convert to tuple

    #             # isolate _id, stripping quotes
    #             _id = pline[0].replace('\"', '')
    #             # possible bug here:
    #             # empty quotes register as empty _id when replaced

    #             # if arguments exist beyond _id
    #             pline = pline[2].strip()  # pline is now str
    #             if pline:
    #                 # check for *args or **kwargs
    #                 if pline[0] == '{' and pline[-1] == '}'\
    #                         and type(eval(pline)) is dict:
    #                     _args = pline
    #                 else:
    #                     _args = pline.replace(',', '')
    #                     # _args = _args.replace('\"', '')
    #         line = ' '.join([_cmd, _cls, _id, _args])

    #     except Exception as mess:
    #         pass
    #     finally:
    #         return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        args = args.split()
        if not args:
            print("** class name missing **")
            return
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        cls_name = args[0]
        new_instance = HBNBCommand.classes[cls_name]()
        for pair in args[1:]:
            pair = pair.split(sep='=')
            name = pair[0]
            value = pair[1]
            parsed_value = parse_value(value)
            if parsed_value is not None:
                setattr(new_instance, name, parsed_value)
            else:
                continue
        print(new_instance.id)
        new_instance.save()

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """Show the string representation of an instance with
        class name and id"""
        args = args.split()
        args_len = len(args)

        if args_len == 0:
            print("** class name missing **")
        elif args_len >= 1 and args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif args_len < 2:
            print("** instance id missing **")
        elif args_len >= 2 and f"{args[0]}.{args[1]}" not in storage.all():
            print("** no instance found **")
        else:
            obj = storage.all()[f"{args[0]}.{args[1]}"]
            print(obj)

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """delete an instance"""
        args = args.split()
        args_len = len(args)

        if args_len == 0:
            print("** class name missing **")
        elif args_len >= 1 and args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif args_len < 2:
            print("** instance id missing **")
        elif args_len >= 2 and f"{args[0]}.{args[1]}" not in storage.all():
            print("** no instance found **")
        else:
            del storage.all()[f"{args[0]}.{args[1]}"]
            storage.save()

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage.all().items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage.all().items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage.all().items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    # def do_update(self, args):
    #     """ Updates a certain object with new info """
    #     c_name = c_id = att_name = att_val = kwargs = ''

    #     # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
    #     args = args.partition(" ")
    #     if args[0]:
    #         c_name = args[0]
    #     else:  # class name not present
    #         print("** class name missing **")
    #         return
    #     if c_name not in HBNBCommand.classes:  # class name invalid
    #         print("** class doesn't exist **")
    #         return

    #     # isolate id from args
    #     args = args[2].partition(" ")
    #     if args[0]:
    #         c_id = args[0]
    #     else:  # id not present
    #         print("** instance id missing **")
    #         return

    #     # generate key from class and id
    #     key = c_name + "." + c_id

    #     # determine if key is present
    #     if key not in storage.all():
    #         print("** no instance found **")
    #         return

    #     # first determine if kwargs or args
    #     if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
    #         kwargs = eval(args[2])
    #         args = [] # reformat kwargs into list, ex: [<name>, <value>, ...]
    #         for k, v in kwargs.items():
    #             args.append(k)
    #             args.append(v)
    #     else:  # isolate args
    #         args = args[2]
    #         if args and args[0] == '\"':  # check for quoted arg
    #             second_quote = args.find('\"', 1)
    #             att_name = args[1:second_quote]
    #             args = args[second_quote + 1:]

    #         args = args.partition(' ')

    #         # if att_name was not quoted arg
    #         if not att_name and args[0] == ' ':
    #             att_name = args[0]
    #         # check for quoted val arg
    #         if args[2] and args[2][0] == '\"':
    #             att_val = args[2][1:args[2].find('\"', 1)]

    #         # if att_val was not quoted arg
    #         if not att_val and args[2]:
    #             att_val = args[2].partition(' ')[0]

    #         args = [att_name, att_val]

    #     # retrieve dictionary of current objects
    #     new_dict = storage.all()[key]

    #     # iterate through attr names and values
    #     for i, att_name in enumerate(args):
    #         # block only runs on even iterations
    #         if (i % 2 == 0):
    #             att_val = args[i + 1]  # following item is value
    #             if not att_name:  # check for att_name
    #                 print("** attribute name missing **")
    #                 return
    #             if not att_val:  # check for att_value
    #                 print("** value missing **")
    #                 return
    #             # type cast as necessary
    #             if att_name in HBNBCommand.types:
    #                 att_val = HBNBCommand.types[att_name](att_val)

    #             # update dictionary with name, value pair
    #             new_dict.__dict__.update({att_name: att_val})

    #     new_dict.save()  # save updates to file

    def do_update(self, args):
        """Update an attribute of an instance

            Usage: update <class> <id> <attr_name> <value>
        """
        args = args.split()
        args_len = len(args)

        if args_len == 0:
            print("** class name missing **")
        elif args_len >= 1 and args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif args_len < 2:
            print("** instance id missing **")
        elif args_len >= 2 and f"{args[0]}.{args[1]}" not in storage.all():
            print("** no instance found **")
        elif args_len < 3:
            print("** attribute name missing **")
        elif args_len < 4:
            print("** value missing **")
        else:
            model = HBNBCommand.classes[args[0]]
            obj = storage.all()[f"{args[0]}.{args[1]}"]
            value = args[3]
            if hasattr(obj, args[2]):
                attr_type = type(getattr(obj, args[2]))
                value = attr_type(value)
            setattr(obj, args[2], value)
            storage.save()

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
