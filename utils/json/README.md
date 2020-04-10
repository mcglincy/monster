

# JSON Patching

We use jsondiff to maintain and apply patches against the original Monster JSON data.

$ pip install jsondiff

To create a patch between the original JSON file and an edited copy:

$ jsondiff --indent 2 classrec_orig.json classrec.json > classrec.patch
$ jsondiff --indent 2 roomdesc_orig.json roomdesc.json > roomdesc.patch
$ jsondiff --indent 2 spells_orig.json spells.json > spells.patch

To apply a patch against the original:

$ jsonpatch --indent 2 classrec_orig.json classrec.patch > classrec.json
$ jsonpatch --indent 2 roomdesc_orig.json roomdesc.patch > roomdesc.json
$ jsonpatch --indent 2 spells_orig.json spells.patch > spells.json
