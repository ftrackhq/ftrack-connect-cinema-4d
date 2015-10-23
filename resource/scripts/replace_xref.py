import c4d
from c4d import gui
#Welcome to the world of Python


def main():
    if op.CheckType(c4d.Oxref):
        op.SetParameter(c4d.ID_CA_XREF_FILE, '../sphere.c4d', c4d.DESCFLAGS_SET_USERINTERACTION)
        c4d.EventAdd()
        print 'Xref file reference changed'
    else:
        print 'Non-xref object selected'

if __name__=='__main__':
    main()
