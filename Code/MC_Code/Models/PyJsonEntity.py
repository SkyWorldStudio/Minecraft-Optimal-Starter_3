import json
class PyJsonEntity:
    @staticmethod
    def JsonToEntity(jsonstr: str, classobj):
        def handlejsonobj(classobj, jdict: dict):
            for i in classobj.__dict__.keys():
                if (i in jdict.keys()):
                    value = jdict[i]
                    if(value is None):
                        setattr(classobj, i, None)
                        continue
                    if (type(value) == dict):
                        if ("__dict__" not in dir(classobj.__dict__[i])):
                            setattr(classobj, i, value)
                        else:
                            objvalue = handlejsonobj(classobj.__dict__[i], value)
                            setattr(classobj, i, objvalue)
                    elif (type(value) == list):
                        clist = classobj.__dict__[i]
                        if (type(clist) != list or len(clist) == 0):
                            setattr(classobj, i, value)
                        else:
                            arrvalue = handlejsonarray(clist[0], value)
                            setattr(classobj, i, arrvalue)
                    else:
                        setattr(classobj, i, value)
                else:
                    setattr(classobj, i, None)
            return classobj
        def handlejsonarray(classobj, listobj):
            array = []
            for i in listobj:
                if(type(i) == list and type(classobj) == list):
                    array2 = handlejsonarray(classobj[0], i)
                    array.append(array2)
                else:
                    array.append(handlejsonobj(classobj.__class__(), i))
            return array
        jdict = json.loads(jsonstr)
        return handlejsonobj(classobj, jdict)
    
    @staticmethod
    def EntityToJson(classobj):
        def handlejsonobj(classobj):
            jdict:dict = {}
            for i in classobj.__dict__.items():
                if(i[1] is None):
                    continue
                if(type(i[1]) == list):
                    value = handlejsonarray(i[1])
                    jdict[i[0]] = value
                elif("__dict__" in dir(i[1])):
                    value = handlejsonobj(i[1])
                    jdict[i[0]] = value
                else:
                    jdict[i[0]] = i[1]
            return jdict
        
        def handlejsonarray(listobj:list):
            array = []
            for i in listobj:
                value = None
                if(type(i) == list):
                    value = handlejsonarray(i)
                elif("__dict__" in dir(i)):
                    value = handlejsonobj(i)
                else:
                    value = i
                array.append(value)
            return array
        
        return handlejsonobj(classobj)



