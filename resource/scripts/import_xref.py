import c4d
from c4d import gui
#Welcome to the world of Python


def main():
    file_path = '../cube.c4d'

    xrefObject = c4d.BaseObject(c4d.Oxref)
    if not xrefObject:
        return

    doc.InsertObject(xrefObject)
    xrefObject.SetParameter(c4d.ID_CA_XREF_FILE, file_path, c4d.DESCFLAGS_SET_USERINTERACTION)
    c4d.EventAdd()

if __name__=='__main__':
    main()
