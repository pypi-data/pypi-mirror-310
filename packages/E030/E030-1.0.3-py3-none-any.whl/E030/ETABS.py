import comtypes.client

# Desplazamientos de los Centros de Masas
def StoryDisp(Caso_Carga:str):
    try:
        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

        TableVersion = 0
        FieldsKeysIncluded = []     # Cabeceras de la Tabla / Table Headers
        NumberRecords = 0           # Número de Filas de la Tabla / Number Rows of Table
        TableData = []              # Array que contiene toda la información de la Tabla / Array containing all information of Table
        FieldKeyList = []
        GroupName = None

        [FieldKeyList, TableVersion, FieldsKeysIncluded, NumberRecords, TableData, ret] = ETABSModel.DatabaseTables.GetTableForDisplayArray("Point Bays", FieldKeyList, GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)

        cont = 1

        CM_Label = [] # labels o Etiquetas de los Puntos de los Centros de Masas
        CM_Unique = [] # Nombres Unicos de los puntos en los Centros de Masas

        Name = None
        NumberNames = 0
        MyName = []

        [NumberNames, MyName, ret] = ETABSModel.Story.GetNameList(NumberNames, MyName)

        piso = 0

        # --------------------------------------------------------------------
        # AGRUPACIÓN DE LOS PUNTOS DE LOS CM EN LABELS Y UNIQUE NAMES
        #---------------------------------------------------------------------
        for i in range(0, NumberRecords):
            if TableData[cont] == "Yes":
                CM_Label.append(TableData[cont - 1])
                [Name, ret] = ETABSModel.PointObj.GetNameFromLabel(TableData[cont - 1], MyName[piso], Name)        
                CM_Unique.append(Name)        
                piso += 1
            cont += len(FieldsKeysIncluded)

        
        forceUnits = 0 ; lengthUnits = 0 ; temperatureUnits = 0
        [forceUnits, lengthUnits, temperatureUnits, ret] = ETABSModel.GetPresentUnits_2(forceUnits, lengthUnits, temperatureUnits)
        ETABSModel.SetPresentUnits_2(6, 6, 2) # Unidades Tonf, m, C

        Obj = []
        Elm = []
        U1 = [] ; U2 = [] ; U3 = [] ; R1 = [] ; R2 = [] ; R3 = []
        NumberResults = 0
        LoadCase = []
        StepType = []
        StepNum = []

        Desp_Ux = []
        Desp_Uy = []

        Point_U = []
        D_X = []
        D_Y = []
        Story_Point = []
        
        ETABSModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        ETABSModel.Results.Setup.SetCaseSelectedForOutput(Caso_Carga)
        for i in range(0, len(CM_Unique)):
            [NumberResults, Obj, Elm, LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3, ret] = ETABSModel.Results.JointDispl(CM_Unique[i], 0, NumberResults, Obj, Elm, LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3)
            Desp_Ux = [] ; Desp_Uy = []
            for j in range(0, len(U1)):
                Desp_Ux.append(U1[j])
                Desp_Uy.append(U2[j])
            D_X.append(max(Desp_Ux))
            D_Y.append(max(Desp_Uy))
            Point_U.append(CM_Unique[i])
            Story_Point.append(MyName[i])

        ETABSModel.SetPresentUnits_2(forceUnits, lengthUnits, temperatureUnits)

        import pandas as pd

        Data_Desp = {"Punto" : Point_U , "Piso" : Story_Point, "Desp.-X" : D_X, "Desp.-Y" : D_Y}
        Tabla_Desp = pd.DataFrame(Data_Desp)

        return Tabla_Desp
    
    except:
        pass

# 1 -> Sistema Regular || 2 -> Sistema Irregular
# R -> Factor de Reducción Sísmica según Norma
# 1-> Concreto || 2 -> Acero || 3-> Albañilería || 4 -> Madera || 5 -> Muros de Ductilidad Limitada

# Derivas de Piso
def StoryDrift(Caso_Carga:str, sistema:int, R:float, Material:int):
    try:
        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

        TableVersion = 0
        FieldsKeysIncluded = []     # Cabeceras de la Tabla / Table Headers
        NumberRecords = 0           # Número de Filas de la Tabla / Number Rows of Table
        TableData = []              # Array que contiene toda la información de la Tabla / Array containing all information of Table
        FieldKeyList = []
        GroupName = None

        [FieldKeyList, TableVersion, FieldsKeysIncluded, NumberRecords, TableData, ret] = ETABSModel.DatabaseTables.GetTableForDisplayArray("Point Bays", FieldKeyList, GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)

        cont = 1

        CM_Label = [] # labels o Etiquetas de los Puntos de los Centros de Masas
        CM_Unique = [] # Nombres Unicos de los puntos en los Centros de Masas
        Altura_Pisos = [] # Altura de todos los pisos

        Name = None
        NumberNames = 0
        MyName = []
        Height = 0

        [NumberNames, MyName, ret] = ETABSModel.Story.GetNameList(NumberNames, MyName)
        
        piso = 0

        # --------------------------------------------------------------------
        # AGRUPACIÓN DE LOS PUNTOS DE LOS CM EN LABELS Y UNIQUE NAMES
        #---------------------------------------------------------------------
        for i in range(0, NumberRecords):
            if TableData[cont] == "Yes":
                CM_Label.append(TableData[cont - 1])
                [Name, ret] = ETABSModel.PointObj.GetNameFromLabel(TableData[cont - 1], MyName[piso], Name)
                [Height, ret] = ETABSModel.Story.GetHeight(MyName[piso], Height)       
                CM_Unique.append(Name)
                Altura_Pisos.append(Height)
                piso += 1
            cont += len(FieldsKeysIncluded)

        
        forceUnits = 0 ; lengthUnits = 0 ; temperatureUnits = 0
        [forceUnits, lengthUnits, temperatureUnits, ret] = ETABSModel.GetPresentUnits_2(forceUnits, lengthUnits, temperatureUnits)
        ETABSModel.SetPresentUnits_2(6, 6, 2) # Unidades Tonf, m, C

        Obj = []
        Elm = []
        U1 = [] ; U2 = [] ; U3 = [] ; R1 = [] ; R2 = [] ; R3 = []
        NumberResults = 0
        LoadCase = []
        StepType = []
        StepNum = []

        Desp_Ux = []
        Desp_Uy = []

        Point_U = []
        D_X = []
        D_Y = []
        Story_Point = []

        Deriva_Elast_X = []
        Deriva_Elast_Y = []
        Deriva_Inelast_X = []
        Deriva_Inelast_Y = []
        Desp_Rel_X = []
        Desp_Rel_Y = []
        Deriva_Limite = []

        factor = 0
        limite = 0

        if sistema == 1:
            factor = 0.75 * R
        else:
            factor = 0.85 * R
        
        if Material == 1:
            limite = 0.007
        elif Material == 2:
            limite = 0.010
        elif Material == 3:
            limite = 0.005
        elif Material == 4:
            limite = 0.010
        elif Material == 5:
            limite = 0.005

        ETABSModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        ETABSModel.Results.Setup.SetCaseSelectedForOutput(Caso_Carga)
        for i in range(0, len(CM_Unique)):
            [NumberResults, Obj, Elm, LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3, ret] = ETABSModel.Results.JointDispl(CM_Unique[i], 0, NumberResults, Obj, Elm, LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3)
            Desp_Ux = [] ; Desp_Uy = []
            for j in range(0, len(U1)):
                Desp_Ux.append(U1[j])
                Desp_Uy.append(U2[j])
            D_X.append(max(Desp_Ux))
            D_Y.append(max(Desp_Uy))
            Point_U.append(CM_Unique[i])
            Story_Point.append(MyName[i])
            Deriva_Limite.append(limite)

            if len(D_X) > 1:
                Desp_Rel_X.append(D_X[len(D_X)-2] - D_X[len(D_X)-1])
                Desp_Rel_Y.append(D_Y[len(D_Y)-2] - D_Y[len(D_Y)-1])
                Deriva_Elast_X.append((D_X[len(D_X)-2] - D_X[len(D_X)-1]) / Altura_Pisos[i])
                Deriva_Elast_Y.append((D_Y[len(D_Y)-2] - D_Y[len(D_Y)-1]) / Altura_Pisos[i])
                Deriva_Inelast_X.append(factor * (D_X[len(D_X)-2] - D_X[len(D_X)-1]) / Altura_Pisos[i])
                Deriva_Inelast_Y.append(factor * (D_Y[len(D_Y)-2] - D_Y[len(D_Y)-1]) / Altura_Pisos[i])

        Desp_Rel_X.append(D_X[len(D_X)-1])
        Desp_Rel_Y.append(D_Y[len(D_Y)-1])
        Deriva_Elast_X.append(D_X[len(D_X)-1] / Altura_Pisos[len(D_X)-1])
        Deriva_Elast_Y.append(D_Y[len(D_Y)-1] / Altura_Pisos[len(D_X)-1])
        Deriva_Inelast_X.append(factor * D_X[len(D_X)-1] / Altura_Pisos[len(D_X)-1])
        Deriva_Inelast_Y.append(factor * D_Y[len(D_Y)-1] / Altura_Pisos[len(D_X)-1])
        
        ETABSModel.SetPresentUnits_2(forceUnits, lengthUnits, temperatureUnits)
     
        import pandas as pd

        Data_Deriva = {"Punto" : Point_U , "Piso" : Story_Point, "Desp.-X" : D_X, "Desp.-Y" : D_Y, "Desp. Rel.-X" : Desp_Rel_X, "Desp. Rel.-Y" : Desp_Rel_Y,
                     "Der. Elást.-X" : Deriva_Elast_X, "Der. Elást.-Y" : Deriva_Elast_Y, "Der. Inelást.-X" : Deriva_Inelast_X, "Der. Inelást.-Y" : Deriva_Inelast_Y,
                     "Limite" : Deriva_Limite}
        Tabla_Deriva = pd.DataFrame(Data_Deriva)

        return Tabla_Deriva
    
    except:
        pass

# Definición del Sismo Estático
def SeismoUserCoef(NameLoad:str, DirLoad:tuple, Ecc:float, RangeStory:tuple, C:float, k:float):
    try:
        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel
        
        # Definición de Patrón de Carga Sísmica Estática
        ETABSModel.LoadPatterns.Add(NameLoad, 5)

        NumFatalErrors = 0 ; NumErrorMsgs = 0 ; NumWarnMsgs = 0 ; NumInfoMsgs = 0
        ImportLog = None        # Información del resultado de la Importación de Datos a la Tabla
        TableVersion = 1
        FieldsKeysIncluded = [] # Contiene las Cabeceras de la Tabla
        NumberRecords = 0       # Número de Filas que tiene la Tabla
        TableData = []          # Contenido de la Tabla
        GroupName = None

        [TableVersion, FieldsKeysIncluded, NumberRecords, TableData, ret] = ETABSModel.DatabaseTables.GetTableForEditingArray("Load Pattern Definitions - Auto Seismic - User Coefficient", GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)
        
        FieldsKeysIncluded = ["Name", "IsAuto", "XDir", "XDirPlusE", "XDirMinusE", "YDir", "YDirPlusE", "YDirMinusE", 
                      "EccRatio", "TopStory", "BotStory", "OverStory", "OverDiaph", "OverEcc", "C", "K"]
        
        if len(TableData) > 1:
            Table_Old = []
            for j in range(0, len(TableData)):
                Table_Old.append(TableData[j])
            New_Data = [NameLoad, "No", DirLoad[0], DirLoad[1], DirLoad[2], DirLoad[3], DirLoad[4], DirLoad[5], str(Ecc), RangeStory[0], RangeStory[1], None, None, None, str(C), str(k)]
            TableData = Table_Old + New_Data
        else:
            TableData = [NameLoad, "No", DirLoad[0], DirLoad[1], DirLoad[2], DirLoad[3], DirLoad[4], DirLoad[5], str(Ecc), RangeStory[0], RangeStory[1], None, None, None, str(C), str(k)]

        NumberRecords = int(len(TableData) / len(FieldsKeysIncluded))
        [FieldsKeysIncluded, NumberRecords, TableData, ret] = ETABSModel.DatabaseTables.SetTableForEditingArray("Load Pattern Definitions - Auto Seismic - User Coefficient", TableVersion, FieldsKeysIncluded, NumberRecords, TableData)
        [NumFatalErrors, NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog, ret] = ETABSModel.DatabaseTables.ApplyEditedTables(True, NumFatalErrors, NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog)

        return print("Carga Sismica \"" + NameLoad + "\" creada con éxito")

    except:
        return print("La Carga \"" + NameLoad + "\" no pudo crearse")

# Definición del Sismo Dinámico por Espectro de Diseño
def SeismoAMRE():
    try:
        1
    except:
        pass

def k(k_x:float, k_y:float):

    try:
        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

        NumberResults = 0
        LoadCase = [] ; StepType = [] ; StepNum = [] ; Period = [] ; Ux = [] ; Uy = [] ; Uz = [] ; SumUx = [] ; SumUy = [] ; SumUz = [] ; Rx = [] ; Ry = [] ; Rz = [] ; SumRx = [] ; SumRy = [] ; SumRz = []

        ETABSModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        ETABSModel.Results.Setup.SetCaseSelectedForOutput("Modal")
        [NumberResults, LoadCase, StepType, StepNum, Period, Ux, Uy, Uz, SumUx, SumUy, SumUz, Rx, Ry, Rz, SumRx, SumRy, SumRz, ret] = ETABSModel.Results.ModalParticipatingMassRatios(NumberResults, LoadCase, StepType, StepNum, Period, Ux, Uy, Uz, SumUx, SumUy, SumUz, Rx, Ry, Rz, SumRx, SumRy, SumRz)

        for i in range(0, NumberResults):

            if round(max(Ux), 5) == round(Ux[i], 5):

                if Period[i] <= 0.5:
                    k_x = 1
                else:
                    k_x = min(0.75 + 0.5 * Period[i], 2)
                
                break

        for i in range(0, NumberResults):

            if round(max(Uy), 5) == round(Uy[i], 5):

                if Period[i] <= 0.5:
                    k_y = 1
                else:
                    k_y = min(0.75 + 0.5 * Period[i], 2)
                
                break
                
        return 1
    
    except:
        pass


def Z(Zona:int, Z:float):

    try:

        if Zona == 1:
            Z = 0.1
        elif Zona == 2:
            Z = 0.25
        elif Zona == 3:
            Z = 0.35
        elif Zona == 4:
            Z = 0.45

        return Z
    
    except:
        pass

def U(Uso:int, U:float):

    try:

        if Uso == 1:
            U = 1.5
        elif Uso == 2:
            U = 1.3
        elif Uso == 3:
            U = 1

        return U
    
    except:
        pass

def C(C_x:float, C_y:float, TP:float, TL:float):

    try:
        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

        NumberResults = 0
        LoadCase = [] ; StepType = [] ; StepNum = [] ; Period = [] ; Ux = [] ; Uy = [] ; Uz = [] ; SumUx = [] ; SumUy = [] ; SumUz = [] ; Rx = [] ; Ry = [] ; Rz = [] ; SumRx = [] ; SumRy = [] ; SumRz = []

        ETABSModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        ETABSModel.Results.Setup.SetCaseSelectedForOutput("Modal")
        [NumberResults, LoadCase, StepType, StepNum, Period, Ux, Uy, Uz, SumUx, SumUy, SumUz, Rx, Ry, Rz, SumRx, SumRy, SumRz, ret] = ETABSModel.Results.ModalParticipatingMassRatios(NumberResults, LoadCase, StepType, StepNum, Period, Ux, Uy, Uz, SumUx, SumUy, SumUz, Rx, Ry, Rz, SumRx, SumRy, SumRz)

        for i in range(0, NumberResults):
            if round(max(Ux), 5) == round(Ux[i], 5):
                T_x = Period[i]
                if T_x <= TP:
                    C_x = 2.5        
                else:
                    if TP < T_x and T_x <= TL:
                        C_x = 2.5 * TP / T_x
                    else:
                        C_x = 2.5 * TP * TL / pow(T_x, 2)
                break

        for i in range(0, NumberResults):
            if round(max(Uy), 5) == round(Uy[i], 5):
                T_y = Period[i]
                if T_y <= TP:
                    C_y = 2.5        
                else:
                    if TP < T_y and T_y <= TL:
                        C_y = 2.5 * TP / T_y
                    else:
                        C_y = 2.5 * TP * TL / pow(T_y, 2)
                break

        return 1

    except:
        pass

def S(Zona:int, Suelo:int, S:float, TP:float, TL:float):

    try:

        if Suelo == 0:
            S = 0.8
            TP = 0.3
            TL = 3
        elif Suelo == 1:
            S = 1
            TP = 0.4
            TL = 2.5
        elif Suelo == 2:
            if Zona == 1:
                S = 1.6
            elif Zona == 2:
                S = 1.2
            elif Zona == 3:
                S = 1.15
            elif Zona == 4:
                S = 1.05
            TP = 0.6
            TL = 2
        elif Suelo == 3:
            if Zona == 1:
                S = 2
            elif Zona == 2:
                S = 1.4
            elif Zona == 3:
                S = 1.2
            elif Zona == 4:
                S = 1.1
            TP = 1
            TL = 1.6

        return 1
    
    except:
        pass

# Arreglo personalizado de listas de barras
def BarCustom(NameBars:tuple, Diameter:tuple, Area:tuple):
        try:
            ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
            ETABSModel = ETABSObject.SapModel

            NumFatalErrors = 0 ; NumErrorMsgs = 0 ; NumWarnMsgs = 0 ; NumInfoMsgs = 0
            ImportLog = None        # Información del resultado de la Importación de Datos a la Tabla
            TableVersion = 1
            FieldsKeysIncluded = [] # Contiene las Cabeceras de la Tabla
            NumberRecords = 0       # Número de Filas que tiene la Tabla
            TableData = []          # Contenido de la Tabla
            GroupName = None

            [TableVersion, FieldsKeysIncluded, NumberRecords, TableData, ret] = ETABSModel.DatabaseTables.GetTableForEditingArray("Reinforcing Bar Sizes", GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)

            FieldsKeysIncluded = ["Name", "Diameter", "Area", "GUID"] # Cabeceras de la Tabla

            TableData = []

            for i in range(0, len(NameBars)):
                TableData.append(NameBars[i])
                TableData.append(str(Diameter[i]))
                TableData.append(str(Area[i]))
                TableData.append("GDSAGDSAFDASFAGEE")

            NumberRecords = int(len(TableData) / len(FieldsKeysIncluded))
            [FieldsKeysIncluded, NumberRecords, TableData, ret] = ETABSModel.DatabaseTables.SetTableForEditingArray("Reinforcing Bar Sizes", TableVersion, FieldsKeysIncluded, NumberRecords, TableData)
            [NumFatalErrors, NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog, ret] = ETABSModel.DatabaseTables.ApplyEditedTables(True, NumFatalErrors, NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog)

            return print("Personalización de barras exitosa")
        
        except:
            return print("La personalización no se realizó")
    
def ColumnTee():
    return 1

def ColumnEle():
    return 1

def ColumnCircular():
    return 1

def PesoSismicoE030():
    return 1

def SistemaEstructural(LoadName:str):
    
    try:
        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

        ETABSModel.PierLabel.SetPier("Muros")
        ETABSModel.PierLabel.SetPier("Columnas")

        NumberNames = 0
        MyName = [] ; MyLabel = [] ; MyStory = []

        [NumberNames, MyName, ret] = ETABSModel.Story.GetNameList(NumberNames, MyName)

        Piso_1 = MyName[NumberNames-1]

        [NumberNames, MyName, MyLabel, MyStory, ret] = ETABSModel.AreaObj.GetLabelNameList(NumberNames, MyName, MyLabel, MyStory)

        for i in range(0, NumberNames):
            if MyLabel[i][0 : 1] == "W" and MyStory[i] == Piso_1:
                ETABSModel.AreaObj.SetPier(MyName[i], "Muros")


        LabelFr = None
        Story = None

        [NumberNames, MyName, ret] = ETABSModel.FrameObj.GetNameListOnStory(Piso_1, NumberNames, MyName)

        for i in range(0, NumberNames-1):

            [LabelFr, Story, ret] = ETABSModel.FrameObj.GetLabelFromName(MyName[i], LabelFr, Story)
    
            if LabelFr[0 : 1] == "C":
                ETABSModel.FrameObj.SetPier(MyName[i], "Columnas")
            Label = None

        
        forceUnits = 0 ; lengthUnits = 0 ; temperatureUnits = 0
        [forceUnits, lengthUnits, temperatureUnits, ret] = ETABSModel.GetPresentUnits_2(forceUnits, lengthUnits, temperatureUnits)
        ETABSModel.SetPresentUnits_2(6, 6, 2) # Unidades Tonf, m, C

        ETABSModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        ETABSModel.Results.Setup.SetCaseSelectedForOutput(LoadName)

        NumberResults = 0
        StoryName = []
        PierName = []
        LoadCase = []
        Location = []
        P = []
        V2 = []
        V3 = []
        T = []
        M2 = []
        M3 = []

        [NumberResults, StoryName, PierName, LoadCase, Location, P, V2, V3, T, M2, M3, ret] = ETABSModel.Results.PierForce(NumberResults, StoryName, PierName, LoadCase, Location, P, V2, V3, T, M2, M3)

        V_muro = 0
        V_column = 0

        for i in range(0, NumberResults):
            if PierName[i] == "Muros":
                V_muro = V2[i]
            elif PierName[i] == "Columnas":
                V_column = V2[i]

        V_total = V_muro + V_column


        Ratio_Muro = V_muro / V_total
        Ratio_Column = V_column / V_total


        print("V_muro: " + str(round(Ratio_Muro, 4)))
        print("V_columna: " + str(round(Ratio_Column, 4)))
        print("------------------------------------")
        if round(Ratio_Column, 4) >= 0.8:
            print("El sistema es de Pórticos")
        elif round(Ratio_Muro, 4) >= 0.7:
            print("El sistema es de Muros Estructurales")
        elif round(Ratio_Muro) >= 0.2 and round(Ratio_Muro) < 0.7:
            print("El sistema es Dual")

        ETABSModel.SetPresentUnits_2(forceUnits, lengthUnits, temperatureUnits)

    except:
        pass
    

def ZUCSR(Zona:int, Uso:int, Suelo:int, R_x:float, R_y:float, ZUCSR_X:float, ZUCSR_Y):

    # Zona -> 1 = Z1 | 2 = Z2 | 3 = Z3 | 4 = Z4
    # Uso -> 1 = Esencial | 2 = Importante | 3 = Comun
    # Suelo -> 0 = So | 1 = S1 | 2 = S2 | 3 = S3

    try:
        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

        NumberResults = 0
        LoadCase = [] ; StepType = [] ; StepNum = [] ; Period = [] ; Ux = [] ; Uy = [] ; Uz = [] ; SumUx = [] ; SumUy = [] ; SumUz = [] ; Rx = [] ; Ry = [] ; Rz = [] ; SumRx = [] ; SumRy = [] ; SumRz = []

        ETABSModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        ETABSModel.Results.Setup.SetCaseSelectedForOutput("Modal")
        [NumberResults, LoadCase, StepType, StepNum, Period, Ux, Uy, Uz, SumUx, SumUy, SumUz, Rx, Ry, Rz, SumRx, SumRy, SumRz, ret] = ETABSModel.Results.ModalParticipatingMassRatios(NumberResults, LoadCase, StepType, StepNum, Period, Ux, Uy, Uz, SumUx, SumUy, SumUz, Rx, Ry, Rz, SumRx, SumRy, SumRz)

        Z = 0 ; U = 0 ; C_x = 0 ; C_y = 0 ; S = 0 ; TP = 0 ; TL = 0
        
        if Zona == 1:
            Z = 0.1
        elif Zona == 2:
            Z = 0.25
        elif Zona == 3:
            Z = 0.35
        elif Zona == 4:
            Z = 0.45


        if Suelo == 0:
            S = 0.8
            TP = 0.3
            TL = 3
        elif Suelo == 1:
            S = 1
            TP = 0.4
            TL = 2.5
        elif Suelo == 2:
            if Zona == 1:
                S = 1.6
            elif Zona == 2:
                S = 1.2
            elif Zona == 3:
                S = 1.15
            elif Zona == 4:
                S = 1.05
            TP = 0.6
            TL = 2
        elif Suelo == 3:
            if Zona == 1:
                S = 2
            elif Zona == 2:
                S = 1.4
            elif Zona == 3:
                S = 1.2
            elif Zona == 4:
                S = 1.1
            TP = 1
            TL = 1.6

        if Uso == 1:
            U = 1.5
        elif Uso == 2:
            U = 1.3
        elif Uso == 3:
            U = 1

        C_x = 0
        C_y = 0

        for i in range(0, NumberResults):
            if round(max(Ux), 5) == round(Ux[i], 5):
                T_x = Period[i]
                if T_x <= TP:
                    C_x = 2.5        
                else:
                    if TP < T_x and T_x <= TL:
                        C_x = 2.5 * TP / T_x
                    else:
                        C_x = 2.5 * TP * TL / pow(T_x, 2)
                break

        for i in range(0, NumberResults):
            if round(max(Uy), 5) == round(Uy[i], 5):
                T_y = Period[i]
                if T_y <= TP:
                    C_y = 2.5        
                else:
                    if TP < T_y and T_y <= TL:
                        C_y = 2.5 * TP / T_y
                    else:
                        C_y = 2.5 * TP * TL / pow(T_y, 2)
                break

        ZUCSR_X = Z * U * C_x * S / R_x
        ZUCSR_Y = Z * U * C_y * S / R_y

        return 1

    except:
        pass

def CombosE060(Load:tuple):

    # Load = 1  -> 1.4CM + 1.7CV
    # Load = 2  -> 1.25(CM + CV ± CVi)
    # Load = 3  -> 0.9CM ± 1.25CVi
    # Load = 4  -> 1.25(CM + CV) ± CS
    # Load = 5  -> 0.9CM ± CS
    # Load = 6  -> 1.4CM + 1.7CV + 1.7CE
    # Load = 7  -> 0.9CM + 1.7CE
    # Load = 8  -> 1.4CM + 1.7CV + 1.7CL
    # Load = 9  -> 1.05CM + 1.25CV 1.05CT
    # Load = 10 -> 1.4CM + 1.7CT

    try:
        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel



    except:
        pass

def CombosE070():
    try:
        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

    except:
        pass

def CombosE090():
    try:
        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

    except:
        pass

def MatAlbaE070():
    try:
        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

    except:
        pass

def MeshSlabs():
    try:
        1
    except:
        pass

def MeshWalls():
    try:
        1
    except:
        pass

def IrregularidadAltura():
    try:
        1
    except:
        pass

def IrregularidadPlanta():
    try:
        1
    except:
        pass

def EmpujeLateral():
    try:
        1
    except:
        pass

def CombosE060forVg():
    try:
        1
    except:
        pass

