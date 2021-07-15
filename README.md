# Replace short PHP tags

Can replace all short php tags in a file or in all files in directory.

Replaces "<?=" with "<?php echo " and "<?" with "<?php "

### Command line arguments
* <file_name> &nbsp;&nbsp;&nbsp;&nbsp;&mdash;  specify the file name. Can be either a relative or absolute path
* <dir_name> &nbsp;&nbsp;&nbsp;&nbsp;&mdash;  specify the directory name. Can be either a relative or absolute path
* -c  &nbsp;&nbsp;&nbsp;&nbsp;&mdash; only check for short PHP tags

If '-c' arg is not specified, than script will replace all occurrences in specified files and/or directories

If a directory is specified, than it will not overwrite the files in directory, but put processed files into 'processed' folder under the specified directory.

If a file is specified, it will not overwrite it as well, it will create a new file named 'processed_<file_name>.php'.
