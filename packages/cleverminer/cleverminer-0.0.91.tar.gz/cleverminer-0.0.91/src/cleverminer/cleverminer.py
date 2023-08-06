import time #line:1
from time import strftime #line:3
from time import gmtime #line:4
import pandas as pd #line:6
class cleverminer :#line:8
    version_string ="0.0.91"#line:10
    def __init__ (O0O0OOOO0OO000000 ,**OO0OOO0O00O000O00 ):#line:12
        O0O0OOOO0OO000000 ._print_disclaimer ()#line:13
        O0O0OOOO0OO000000 .stats ={'total_cnt':0 ,'total_valid':0 ,'control_number':0 ,'start_prep_time':time .time (),'end_prep_time':time .time (),'start_proc_time':time .time (),'end_proc_time':time .time ()}#line:21
        O0O0OOOO0OO000000 ._init_data ()#line:22
        O0O0OOOO0OO000000 ._init_task ()#line:23
        if len (OO0OOO0O00O000O00 )>0 :#line:24
            O0O0OOOO0OO000000 .kwargs =OO0OOO0O00O000O00 #line:25
            O0O0OOOO0OO000000 ._calc_all (**OO0OOO0O00O000O00 )#line:26
    def _init_data (OO00O0OO0O000000O ):#line:28
        OO00O0OO0O000000O .data ={}#line:30
        OO00O0OO0O000000O .data ["varname"]=[]#line:31
        OO00O0OO0O000000O .data ["catnames"]=[]#line:32
        OO00O0OO0O000000O .data ["vtypes"]=[]#line:33
        OO00O0OO0O000000O .data ["dm"]=[]#line:34
        OO00O0OO0O000000O .data ["rows_count"]=int (0 )#line:35
        OO00O0OO0O000000O .data ["data_prepared"]=0 #line:36
    def _init_task (O00O000OOO00O0OOO ):#line:38
        O00O000OOO00O0OOO .cedent ={'cedent_type':'none','defi':{},'num_cedent':0 ,'trace_cedent':[],'traces':[],'generated_string':'','filter_value':int (0 )}#line:47
        O00O000OOO00O0OOO .task_actinfo ={'proc':'','cedents_to_do':[],'cedents':[]}#line:51
        O00O000OOO00O0OOO .rulelist =[]#line:52
        O00O000OOO00O0OOO .stats ['total_cnt']=0 #line:54
        O00O000OOO00O0OOO .stats ['total_valid']=0 #line:55
        O00O000OOO00O0OOO .stats ['control_number']=0 #line:56
        O00O000OOO00O0OOO .result ={}#line:57
    def _get_ver (O00O0OO00O0O0OO00 ):#line:59
        return O00O0OO00O0O0OO00 .version_string #line:60
    def _print_disclaimer (O00OO0O0O0O0OO00O ):#line:62
        print ("***********************************************************************************************************************************************************************")#line:63
        print ("Cleverminer version ",O00OO0O0O0O0OO00O ._get_ver ())#line:64
        print ("IMPORTANT NOTE: this is preliminary development version of CleverMiner procedure. This procedure is under intensive development and early released for educational use,")#line:65
        print ("    so there is ABSOLUTELY no guarantee of results, possible gaps in functionality and no guarantee of keeping syntax and parameters as in current version.")#line:66
        print ("    (That means we need to tidy up and make proper design, input validation, documentation and instrumentation before launch)")#line:67
        print ("This version is for personal and educational use only.")#line:68
        print ("***********************************************************************************************************************************************************************")#line:69
    def _prep_data (O00O000O0OOO00O00 ,OO0O000O00OO00O0O ):#line:71
        print ("Starting data preparation ...")#line:72
        O00O000O0OOO00O00 ._init_data ()#line:73
        O00O000O0OOO00O00 .stats ['start_prep_time']=time .time ()#line:74
        O00O000O0OOO00O00 .data ["rows_count"]=OO0O000O00OO00O0O .shape [0 ]#line:75
        for OOO0OO0O0O00OOO0O in OO0O000O00OO00O0O .select_dtypes (exclude =['category']).columns :#line:76
            OO0O000O00OO00O0O [OOO0OO0O0O00OOO0O ]=OO0O000O00OO00O0O [OOO0OO0O0O00OOO0O ].apply (str )#line:77
        try :#line:78
            OO0O00OO0OOOOOOO0 =pd .DataFrame .from_records ([(OO00O0O0O0O0O0OOO ,OO0O000O00OO00O0O [OO00O0O0O0O0O0OOO ].nunique ())for OO00O0O0O0O0O0OOO in OO0O000O00OO00O0O .columns ],columns =['Column_Name','Num_Unique']).sort_values (by =['Num_Unique'])#line:80
        except :#line:81
            print ("Error in input data, probably unsupported data type. Will try to scan for column with unsupported type.")#line:82
            OO00OOOOO0OO00OOO =""#line:83
            try :#line:84
                for OOO0OO0O0O00OOO0O in OO0O000O00OO00O0O .columns :#line:85
                    OO00OOOOO0OO00OOO =OOO0OO0O0O00OOO0O #line:87
                    print (f"...column {OOO0OO0O0O00OOO0O} has {int(OO0O000O00OO00O0O[OOO0OO0O0O00OOO0O].nunique())} values")#line:88
            except :#line:89
                print (f"... detected : column {OO00OOOOO0OO00OOO} has unsupported type: {type(OO0O000O00OO00O0O[OOO0OO0O0O00OOO0O])}.")#line:90
                exit (1 )#line:91
            print (f"Error in data profiling - attribute with unsupported type not detected. Please profile attributes manually, only simple attributes are supported.")#line:92
            exit (1 )#line:93
        print ("Unique value counts are:")#line:94
        print (OO0O00OO0OOOOOOO0 )#line:95
        for OOO0OO0O0O00OOO0O in OO0O000O00OO00O0O .columns :#line:96
            if OO0O000O00OO00O0O [OOO0OO0O0O00OOO0O ].nunique ()<100 :#line:97
                OO0O000O00OO00O0O [OOO0OO0O0O00OOO0O ]=OO0O000O00OO00O0O [OOO0OO0O0O00OOO0O ].astype ('category')#line:98
            else :#line:99
                print (f"WARNING: attribute {OOO0OO0O0O00OOO0O} has more than 100 values, will be ignored.")#line:100
                del OO0O000O00OO00O0O [OOO0OO0O0O00OOO0O ]#line:101
        print ("Encoding columns into bit-form...")#line:102
        O0OO00000O0OO0OO0 =0 #line:103
        O0O00O00OOO0O0OO0 =0 #line:104
        for OO0O0O00O000O00OO in OO0O000O00OO00O0O :#line:105
            print ('Column: '+OO0O0O00O000O00OO )#line:107
            O00O000O0OOO00O00 .data ["varname"].append (OO0O0O00O000O00OO )#line:108
            OO0O0O00000000OOO =pd .get_dummies (OO0O000O00OO00O0O [OO0O0O00O000O00OO ])#line:109
            OOO000000000OO000 =0 #line:110
            if (OO0O000O00OO00O0O .dtypes [OO0O0O00O000O00OO ].name =='category'):#line:111
                OOO000000000OO000 =1 #line:112
            O00O000O0OOO00O00 .data ["vtypes"].append (OOO000000000OO000 )#line:113
            O00OO0O00OOO00O00 =0 #line:116
            OO00O000OO00O0OOO =[]#line:117
            O00O00O000O0OO0OO =[]#line:118
            for O0OOOO00000O0O0OO in OO0O0O00000000OOO :#line:120
                print ('....category : '+str (O0OOOO00000O0O0OO )+" @ "+str (time .time ()))#line:122
                OO00O000OO00O0OOO .append (O0OOOO00000O0O0OO )#line:123
                OO0O00O0OO0O000O0 =int (0 )#line:124
                OO000000O0O00O00O =OO0O0O00000000OOO [O0OOOO00000O0O0OO ].values #line:125
                for OOO0O00O00OO0OOO0 in range (O00O000O0OOO00O00 .data ["rows_count"]):#line:127
                    if OO000000O0O00O00O [OOO0O00O00OO0OOO0 ]>0 :#line:128
                        OO0O00O0OO0O000O0 +=1 <<OOO0O00O00OO0OOO0 #line:129
                O00O00O000O0OO0OO .append (OO0O00O0OO0O000O0 )#line:130
                O00OO0O00OOO00O00 +=1 #line:140
                O0O00O00OOO0O0OO0 +=1 #line:141
            O00O000O0OOO00O00 .data ["catnames"].append (OO00O000OO00O0OOO )#line:143
            O00O000O0OOO00O00 .data ["dm"].append (O00O00O000O0OO0OO )#line:144
        print ("Encoding columns into bit-form...done")#line:146
        print ("Encoding columns into bit-form...done")#line:147
        print (f"List of attributes for analysis is: {O00O000O0OOO00O00.data['varname']}")#line:148
        print (f"List of category names for individual attributes is : {O00O000O0OOO00O00.data['catnames']}")#line:149
        print (f"List of vtypes is (all should be 1) : {O00O000O0OOO00O00.data['vtypes']}")#line:150
        O00O000O0OOO00O00 .data ["data_prepared"]=1 #line:152
        print ("Data preparation finished ...")#line:153
        print ('Number of variables : '+str (len (O00O000O0OOO00O00 .data ["dm"])))#line:154
        print ('Total number of categories in all variables : '+str (O0O00O00OOO0O0OO0 ))#line:155
        O00O000O0OOO00O00 .stats ['end_prep_time']=time .time ()#line:156
        print ('Time needed for data preparation : ',str (O00O000O0OOO00O00 .stats ['end_prep_time']-O00O000O0OOO00O00 .stats ['start_prep_time']))#line:157
    def bitcount (O00O00OO0OOOO0OO0 ,O0OOOO0OO0000OO00 ):#line:160
        OO000OO00OO0O000O =0 #line:161
        while O0OOOO0OO0000OO00 >0 :#line:162
            if (O0OOOO0OO0000OO00 &1 ==1 ):OO000OO00OO0O000O +=1 #line:163
            O0OOOO0OO0000OO00 >>=1 #line:164
        return OO000OO00OO0O000O #line:165
    def _verifyCF (O0O00OOO0OO0OOO0O ,_O0OO0000O0OOOO000 ):#line:168
        OOOOOO0O0OOO0O0O0 =bin (_O0OO0000O0OOOO000 ).count ("1")#line:169
        OOO000O0O0OOO0OOO =[]#line:170
        O00OOO0O00O0OOOO0 =[]#line:171
        OO0O00O00000O0OO0 =0 #line:172
        OO0O000000OOOO00O =0 #line:173
        O0OO00O00OOOO0O00 =0 #line:174
        O000O0OOO000OO0O0 =0 #line:175
        OOO0O0OOO0000O0O0 =0 #line:176
        O00OOOOOO000OOO0O =0 #line:177
        OO0O0OOOO0O0OOOOO =0 #line:178
        OO0O0O00O0O00O0OO =0 #line:179
        O0O00OOOOOO0O000O =0 #line:180
        OO00O0O0OOOOO0OO0 =O0O00OOO0OO0OOO0O .data ["dm"][O0O00OOO0OO0OOO0O .data ["varname"].index (O0O00OOO0OO0OOO0O .kwargs .get ('target'))]#line:181
        for OO000O00O000O0O00 in range (len (OO00O0O0OOOOO0OO0 )):#line:182
            OO0O000000OOOO00O =OO0O00O00000O0OO0 #line:183
            OO0O00O00000O0OO0 =bin (_O0OO0000O0OOOO000 &OO00O0O0OOOOO0OO0 [OO000O00O000O0O00 ]).count ("1")#line:184
            OOO000O0O0OOO0OOO .append (OO0O00O00000O0OO0 )#line:185
            if OO000O00O000O0O00 >0 :#line:186
                if (OO0O00O00000O0OO0 >OO0O000000OOOO00O ):#line:187
                    if (O0OO00O00OOOO0O00 ==1 ):#line:188
                        OO0O0O00O0O00O0OO +=1 #line:189
                    else :#line:190
                        OO0O0O00O0O00O0OO =1 #line:191
                    if OO0O0O00O0O00O0OO >O000O0OOO000OO0O0 :#line:192
                        O000O0OOO000OO0O0 =OO0O0O00O0O00O0OO #line:193
                    O0OO00O00OOOO0O00 =1 #line:194
                    O00OOOOOO000OOO0O +=1 #line:195
                if (OO0O00O00000O0OO0 <OO0O000000OOOO00O ):#line:196
                    if (O0OO00O00OOOO0O00 ==-1 ):#line:197
                        O0O00OOOOOO0O000O +=1 #line:198
                    else :#line:199
                        O0O00OOOOOO0O000O =1 #line:200
                    if O0O00OOOOOO0O000O >OOO0O0OOO0000O0O0 :#line:201
                        OOO0O0OOO0000O0O0 =O0O00OOOOOO0O000O #line:202
                    O0OO00O00OOOO0O00 =-1 #line:203
                    OO0O0OOOO0O0OOOOO +=1 #line:204
                if (OO0O00O00000O0OO0 ==OO0O000000OOOO00O ):#line:205
                    O0OO00O00OOOO0O00 =0 #line:206
                    O0O00OOOOOO0O000O =0 #line:207
                    OO0O0O00O0O00O0OO =0 #line:208
        O0O0OO00OOO0O00O0 =True #line:211
        for OO00O000O00000OO0 in O0O00OOO0OO0OOO0O .quantifiers .keys ():#line:212
            if OO00O000O00000OO0 .upper ()=='BASE':#line:213
                O0O0OO00OOO0O00O0 =O0O0OO00OOO0O00O0 and (O0O00OOO0OO0OOO0O .quantifiers .get (OO00O000O00000OO0 )<=OOOOOO0O0OOO0O0O0 )#line:214
            if OO00O000O00000OO0 .upper ()=='RELBASE':#line:215
                O0O0OO00OOO0O00O0 =O0O0OO00OOO0O00O0 and (O0O00OOO0OO0OOO0O .quantifiers .get (OO00O000O00000OO0 )<=OOOOOO0O0OOO0O0O0 *1.0 /O0O00OOO0OO0OOO0O .data ["rows_count"])#line:216
            if OO00O000O00000OO0 .upper ()=='S_UP':#line:217
                O0O0OO00OOO0O00O0 =O0O0OO00OOO0O00O0 and (O0O00OOO0OO0OOO0O .quantifiers .get (OO00O000O00000OO0 )<=O000O0OOO000OO0O0 )#line:218
            if OO00O000O00000OO0 .upper ()=='S_DOWN':#line:219
                O0O0OO00OOO0O00O0 =O0O0OO00OOO0O00O0 and (O0O00OOO0OO0OOO0O .quantifiers .get (OO00O000O00000OO0 )<=OOO0O0OOO0000O0O0 )#line:220
            if OO00O000O00000OO0 .upper ()=='S_ANY_UP':#line:221
                O0O0OO00OOO0O00O0 =O0O0OO00OOO0O00O0 and (O0O00OOO0OO0OOO0O .quantifiers .get (OO00O000O00000OO0 )<=O000O0OOO000OO0O0 )#line:222
            if OO00O000O00000OO0 .upper ()=='S_ANY_DOWN':#line:223
                O0O0OO00OOO0O00O0 =O0O0OO00OOO0O00O0 and (O0O00OOO0OO0OOO0O .quantifiers .get (OO00O000O00000OO0 )<=OOO0O0OOO0000O0O0 )#line:224
            if OO00O000O00000OO0 .upper ()=='MAX':#line:225
                O0O0OO00OOO0O00O0 =O0O0OO00OOO0O00O0 and (O0O00OOO0OO0OOO0O .quantifiers .get (OO00O000O00000OO0 )<=max (OOO000O0O0OOO0OOO ))#line:226
            if OO00O000O00000OO0 .upper ()=='MIN':#line:227
                O0O0OO00OOO0O00O0 =O0O0OO00OOO0O00O0 and (O0O00OOO0OO0OOO0O .quantifiers .get (OO00O000O00000OO0 )<=min (OOO000O0O0OOO0OOO ))#line:228
            if OO00O000O00000OO0 .upper ()=='RELMAX':#line:229
                if sum (OOO000O0O0OOO0OOO )>0 :#line:230
                    O0O0OO00OOO0O00O0 =O0O0OO00OOO0O00O0 and (O0O00OOO0OO0OOO0O .quantifiers .get (OO00O000O00000OO0 )<=max (OOO000O0O0OOO0OOO )*1.0 /sum (OOO000O0O0OOO0OOO ))#line:231
                else :#line:232
                    O0O0OO00OOO0O00O0 =False #line:233
            if OO00O000O00000OO0 .upper ()=='RELMAX_LEQ':#line:234
                if sum (OOO000O0O0OOO0OOO )>0 :#line:235
                    O0O0OO00OOO0O00O0 =O0O0OO00OOO0O00O0 and (O0O00OOO0OO0OOO0O .quantifiers .get (OO00O000O00000OO0 )>=max (OOO000O0O0OOO0OOO )*1.0 /sum (OOO000O0O0OOO0OOO ))#line:236
                else :#line:237
                    O0O0OO00OOO0O00O0 =False #line:238
            if OO00O000O00000OO0 .upper ()=='RELMIN':#line:239
                if sum (OOO000O0O0OOO0OOO )>0 :#line:240
                    O0O0OO00OOO0O00O0 =O0O0OO00OOO0O00O0 and (O0O00OOO0OO0OOO0O .quantifiers .get (OO00O000O00000OO0 )<=min (OOO000O0O0OOO0OOO )*1.0 /sum (OOO000O0O0OOO0OOO ))#line:241
                else :#line:242
                    O0O0OO00OOO0O00O0 =False #line:243
            if OO00O000O00000OO0 .upper ()=='RELMIN_LEQ':#line:244
                if sum (OOO000O0O0OOO0OOO )>0 :#line:245
                    O0O0OO00OOO0O00O0 =O0O0OO00OOO0O00O0 and (O0O00OOO0OO0OOO0O .quantifiers .get (OO00O000O00000OO0 )>=min (OOO000O0O0OOO0OOO )*1.0 /sum (OOO000O0O0OOO0OOO ))#line:246
                else :#line:247
                    O0O0OO00OOO0O00O0 =False #line:248
        O00O0O0000OOO0OOO ={}#line:249
        if O0O0OO00OOO0O00O0 ==True :#line:250
            O0O00OOO0OO0OOO0O .stats ['total_valid']+=1 #line:252
            O00O0O0000OOO0OOO ["base"]=OOOOOO0O0OOO0O0O0 #line:253
            O00O0O0000OOO0OOO ["rel_base"]=OOOOOO0O0OOO0O0O0 *1.0 /O0O00OOO0OO0OOO0O .data ["rows_count"]#line:254
            O00O0O0000OOO0OOO ["s_up"]=O000O0OOO000OO0O0 #line:255
            O00O0O0000OOO0OOO ["s_down"]=OOO0O0OOO0000O0O0 #line:256
            O00O0O0000OOO0OOO ["s_any_up"]=O00OOOOOO000OOO0O #line:257
            O00O0O0000OOO0OOO ["s_any_down"]=OO0O0OOOO0O0OOOOO #line:258
            O00O0O0000OOO0OOO ["max"]=max (OOO000O0O0OOO0OOO )#line:259
            O00O0O0000OOO0OOO ["min"]=min (OOO000O0O0OOO0OOO )#line:260
            if sum (OOO000O0O0OOO0OOO )>0 :#line:263
                O00O0O0000OOO0OOO ["rel_max"]=max (OOO000O0O0OOO0OOO )*1.0 /sum (OOO000O0O0OOO0OOO )#line:264
                O00O0O0000OOO0OOO ["rel_min"]=min (OOO000O0O0OOO0OOO )*1.0 /sum (OOO000O0O0OOO0OOO )#line:265
            else :#line:266
                O00O0O0000OOO0OOO ["rel_max"]=0 #line:267
                O00O0O0000OOO0OOO ["rel_min"]=0 #line:268
            O00O0O0000OOO0OOO ["hist"]=OOO000O0O0OOO0OOO #line:269
        return O0O0OO00OOO0O00O0 ,O00O0O0000OOO0OOO #line:271
    def _verify4ft (O0O00OOOOOO000O0O ,_OO0OOO00O0O0000OO ):#line:273
        O0O000OO0O00O0000 ={}#line:274
        OOO0O0OO00O000OOO =0 #line:275
        for O0O0OOO0O00000OOO in O0O00OOOOOO000O0O .task_actinfo ['cedents']:#line:276
            O0O000OO0O00O0000 [O0O0OOO0O00000OOO ['cedent_type']]=O0O0OOO0O00000OOO ['filter_value']#line:278
            OOO0O0OO00O000OOO =OOO0O0OO00O000OOO +1 #line:279
        O0O000O0O0OO0O0O0 =bin (O0O000OO0O00O0000 ['ante']&O0O000OO0O00O0000 ['succ']&O0O000OO0O00O0000 ['cond']).count ("1")#line:281
        O0O000OOOOO0O0OOO =None #line:282
        O0O000OOOOO0O0OOO =0 #line:283
        if O0O000O0O0OO0O0O0 >0 :#line:292
            O0O000OOOOO0O0OOO =bin (O0O000OO0O00O0000 ['ante']&O0O000OO0O00O0000 ['succ']&O0O000OO0O00O0000 ['cond']).count ("1")*1.0 /bin (O0O000OO0O00O0000 ['ante']&O0O000OO0O00O0000 ['cond']).count ("1")#line:293
        OOO0000OO00OO0O0O =1 <<O0O00OOOOOO000O0O .data ["rows_count"]#line:295
        OOOOOOO0O0O00O0OO =bin (O0O000OO0O00O0000 ['ante']&O0O000OO0O00O0000 ['succ']&O0O000OO0O00O0000 ['cond']).count ("1")#line:296
        O0000OO0O000O0OO0 =bin (O0O000OO0O00O0000 ['ante']&~(OOO0000OO00OO0O0O |O0O000OO0O00O0000 ['succ'])&O0O000OO0O00O0000 ['cond']).count ("1")#line:297
        O0O0OOO0O00000OOO =bin (~(OOO0000OO00OO0O0O |O0O000OO0O00O0000 ['ante'])&O0O000OO0O00O0000 ['succ']&O0O000OO0O00O0000 ['cond']).count ("1")#line:298
        OO0O00O0O00OOOOO0 =bin (~(OOO0000OO00OO0O0O |O0O000OO0O00O0000 ['ante'])&~(OOO0000OO00OO0O0O |O0O000OO0O00O0000 ['succ'])&O0O000OO0O00O0000 ['cond']).count ("1")#line:299
        O00OO0OO0O0000O0O =0 #line:300
        if (OOOOOOO0O0O00O0OO +O0000OO0O000O0OO0 )*(OOOOOOO0O0O00O0OO +O0O0OOO0O00000OOO )>0 :#line:301
            O00OO0OO0O0000O0O =OOOOOOO0O0O00O0OO *(OOOOOOO0O0O00O0OO +O0000OO0O000O0OO0 +O0O0OOO0O00000OOO +OO0O00O0O00OOOOO0 )/(OOOOOOO0O0O00O0OO +O0000OO0O000O0OO0 )/(OOOOOOO0O0O00O0OO +O0O0OOO0O00000OOO )-1 #line:302
        else :#line:303
            O00OO0OO0O0000O0O =None #line:304
        OO000O000O00OO0O0 =0 #line:305
        if (OOOOOOO0O0O00O0OO +O0000OO0O000O0OO0 )*(OOOOOOO0O0O00O0OO +O0O0OOO0O00000OOO )>0 :#line:306
            OO000O000O00OO0O0 =1 -OOOOOOO0O0O00O0OO *(OOOOOOO0O0O00O0OO +O0000OO0O000O0OO0 +O0O0OOO0O00000OOO +OO0O00O0O00OOOOO0 )/(OOOOOOO0O0O00O0OO +O0000OO0O000O0OO0 )/(OOOOOOO0O0O00O0OO +O0O0OOO0O00000OOO )#line:307
        else :#line:308
            OO000O000O00OO0O0 =None #line:309
        OOOOO0OOO00OOO0OO =True #line:310
        for OO00O00OOOOOO000O in O0O00OOOOOO000O0O .quantifiers .keys ():#line:311
            if OO00O00OOOOOO000O .upper ()=='BASE':#line:312
                OOOOO0OOO00OOO0OO =OOOOO0OOO00OOO0OO and (O0O00OOOOOO000O0O .quantifiers .get (OO00O00OOOOOO000O )<=O0O000O0O0OO0O0O0 )#line:313
            if OO00O00OOOOOO000O .upper ()=='RELBASE':#line:314
                OOOOO0OOO00OOO0OO =OOOOO0OOO00OOO0OO and (O0O00OOOOOO000O0O .quantifiers .get (OO00O00OOOOOO000O )<=O0O000O0O0OO0O0O0 *1.0 /O0O00OOOOOO000O0O .data ["rows_count"])#line:315
            if (OO00O00OOOOOO000O .upper ()=='PIM')or (OO00O00OOOOOO000O .upper ()=='CONF'):#line:316
                OOOOO0OOO00OOO0OO =OOOOO0OOO00OOO0OO and (O0O00OOOOOO000O0O .quantifiers .get (OO00O00OOOOOO000O )<=O0O000OOOOO0O0OOO )#line:317
            if OO00O00OOOOOO000O .upper ()=='AAD':#line:318
                if O00OO0OO0O0000O0O !=None :#line:319
                    OOOOO0OOO00OOO0OO =OOOOO0OOO00OOO0OO and (O0O00OOOOOO000O0O .quantifiers .get (OO00O00OOOOOO000O )<=O00OO0OO0O0000O0O )#line:320
                else :#line:321
                    OOOOO0OOO00OOO0OO =False #line:322
            if OO00O00OOOOOO000O .upper ()=='BAD':#line:323
                if OO000O000O00OO0O0 !=None :#line:324
                    OOOOO0OOO00OOO0OO =OOOOO0OOO00OOO0OO and (O0O00OOOOOO000O0O .quantifiers .get (OO00O00OOOOOO000O )<=OO000O000O00OO0O0 )#line:325
                else :#line:326
                    OOOOO0OOO00OOO0OO =False #line:327
            OOO0OO0OO0OOO0O00 ={}#line:328
        if OOOOO0OOO00OOO0OO ==True :#line:329
            O0O00OOOOOO000O0O .stats ['total_valid']+=1 #line:331
            OOO0OO0OO0OOO0O00 ["base"]=O0O000O0O0OO0O0O0 #line:332
            OOO0OO0OO0OOO0O00 ["rel_base"]=O0O000O0O0OO0O0O0 *1.0 /O0O00OOOOOO000O0O .data ["rows_count"]#line:333
            OOO0OO0OO0OOO0O00 ["conf"]=O0O000OOOOO0O0OOO #line:334
            OOO0OO0OO0OOO0O00 ["aad"]=O00OO0OO0O0000O0O #line:335
            OOO0OO0OO0OOO0O00 ["bad"]=OO000O000O00OO0O0 #line:336
            OOO0OO0OO0OOO0O00 ["fourfold"]=[OOOOOOO0O0O00O0OO ,O0000OO0O000O0OO0 ,O0O0OOO0O00000OOO ,OO0O00O0O00OOOOO0 ]#line:337
        return OOOOO0OOO00OOO0OO ,OOO0OO0OO0OOO0O00 #line:341
    def _verifysd4ft (O0OO0O00OO00O0OO0 ,_O0O00OOOOO00OO000 ):#line:343
        O0O000OO0OO000O0O ={}#line:344
        OOO00OOO0OOOOO00O =0 #line:345
        for OO0OOOO000OOO00OO in O0OO0O00OO00O0OO0 .task_actinfo ['cedents']:#line:346
            O0O000OO0OO000O0O [OO0OOOO000OOO00OO ['cedent_type']]=OO0OOOO000OOO00OO ['filter_value']#line:348
            OOO00OOO0OOOOO00O =OOO00OOO0OOOOO00O +1 #line:349
        O0OOO0OOO0OOO0OO0 =bin (O0O000OO0OO000O0O ['ante']&O0O000OO0OO000O0O ['succ']&O0O000OO0OO000O0O ['cond']&O0O000OO0OO000O0O ['frst']).count ("1")#line:351
        OOO0O0OO0O00000O0 =bin (O0O000OO0OO000O0O ['ante']&O0O000OO0OO000O0O ['succ']&O0O000OO0OO000O0O ['cond']&O0O000OO0OO000O0O ['scnd']).count ("1")#line:352
        OO0OOOOOOOOOOO000 =None #line:353
        OO000OO0OOOO0OO0O =0 #line:354
        OOOO00OOOO0OOOOOO =0 #line:355
        if O0OOO0OOO0OOO0OO0 >0 :#line:364
            OO000OO0OOOO0OO0O =bin (O0O000OO0OO000O0O ['ante']&O0O000OO0OO000O0O ['succ']&O0O000OO0OO000O0O ['cond']&O0O000OO0OO000O0O ['frst']).count ("1")*1.0 /bin (O0O000OO0OO000O0O ['ante']&O0O000OO0OO000O0O ['cond']&O0O000OO0OO000O0O ['frst']).count ("1")#line:365
        if OOO0O0OO0O00000O0 >0 :#line:366
            OOOO00OOOO0OOOOOO =bin (O0O000OO0OO000O0O ['ante']&O0O000OO0OO000O0O ['succ']&O0O000OO0OO000O0O ['cond']&O0O000OO0OO000O0O ['scnd']).count ("1")*1.0 /bin (O0O000OO0OO000O0O ['ante']&O0O000OO0OO000O0O ['cond']&O0O000OO0OO000O0O ['scnd']).count ("1")#line:367
        O00O0000O00000O0O =1 <<O0OO0O00OO00O0OO0 .data ["rows_count"]#line:369
        O0OOO0O00O00O0OOO =bin (O0O000OO0OO000O0O ['ante']&O0O000OO0OO000O0O ['succ']&O0O000OO0OO000O0O ['cond']&O0O000OO0OO000O0O ['frst']).count ("1")#line:370
        O0OO00000OO00O000 =bin (O0O000OO0OO000O0O ['ante']&~(O00O0000O00000O0O |O0O000OO0OO000O0O ['succ'])&O0O000OO0OO000O0O ['cond']&O0O000OO0OO000O0O ['frst']).count ("1")#line:371
        O0OOOOO0O000OOOOO =bin (~(O00O0000O00000O0O |O0O000OO0OO000O0O ['ante'])&O0O000OO0OO000O0O ['succ']&O0O000OO0OO000O0O ['cond']&O0O000OO0OO000O0O ['frst']).count ("1")#line:372
        OOO0OO0O0OO0O000O =bin (~(O00O0000O00000O0O |O0O000OO0OO000O0O ['ante'])&~(O00O0000O00000O0O |O0O000OO0OO000O0O ['succ'])&O0O000OO0OO000O0O ['cond']&O0O000OO0OO000O0O ['frst']).count ("1")#line:373
        OOO0O0OOO0O00OOO0 =bin (O0O000OO0OO000O0O ['ante']&O0O000OO0OO000O0O ['succ']&O0O000OO0OO000O0O ['cond']&O0O000OO0OO000O0O ['scnd']).count ("1")#line:374
        OOO0OOOO0OOO00OOO =bin (O0O000OO0OO000O0O ['ante']&~(O00O0000O00000O0O |O0O000OO0OO000O0O ['succ'])&O0O000OO0OO000O0O ['cond']&O0O000OO0OO000O0O ['scnd']).count ("1")#line:375
        OOO000O0O0000O0O0 =bin (~(O00O0000O00000O0O |O0O000OO0OO000O0O ['ante'])&O0O000OO0OO000O0O ['succ']&O0O000OO0OO000O0O ['cond']&O0O000OO0OO000O0O ['scnd']).count ("1")#line:376
        O0000OO0OOOO0O0O0 =bin (~(O00O0000O00000O0O |O0O000OO0OO000O0O ['ante'])&~(O00O0000O00000O0O |O0O000OO0OO000O0O ['succ'])&O0O000OO0OO000O0O ['cond']&O0O000OO0OO000O0O ['scnd']).count ("1")#line:377
        OO0OO00O0OO00OO0O =True #line:378
        for OO00OO0000OO00OO0 in O0OO0O00OO00O0OO0 .quantifiers .keys ():#line:379
            if (OO00OO0000OO00OO0 .upper ()=='FRSTBASE')|(OO00OO0000OO00OO0 .upper ()=='BASE1'):#line:380
                OO0OO00O0OO00OO0O =OO0OO00O0OO00OO0O and (O0OO0O00OO00O0OO0 .quantifiers .get (OO00OO0000OO00OO0 )<=O0OOO0OOO0OOO0OO0 )#line:381
            if (OO00OO0000OO00OO0 .upper ()=='SCNDBASE')|(OO00OO0000OO00OO0 .upper ()=='BASE2'):#line:382
                OO0OO00O0OO00OO0O =OO0OO00O0OO00OO0O and (O0OO0O00OO00O0OO0 .quantifiers .get (OO00OO0000OO00OO0 )<=OOO0O0OO0O00000O0 )#line:383
            if (OO00OO0000OO00OO0 .upper ()=='FRSTRELBASE')|(OO00OO0000OO00OO0 .upper ()=='RELBASE1'):#line:384
                OO0OO00O0OO00OO0O =OO0OO00O0OO00OO0O and (O0OO0O00OO00O0OO0 .quantifiers .get (OO00OO0000OO00OO0 )<=O0OOO0OOO0OOO0OO0 *1.0 /O0OO0O00OO00O0OO0 .data ["rows_count"])#line:385
            if (OO00OO0000OO00OO0 .upper ()=='SCNDRELBASE')|(OO00OO0000OO00OO0 .upper ()=='RELBASE2'):#line:386
                OO0OO00O0OO00OO0O =OO0OO00O0OO00OO0O and (O0OO0O00OO00O0OO0 .quantifiers .get (OO00OO0000OO00OO0 )<=OOO0O0OO0O00000O0 *1.0 /O0OO0O00OO00O0OO0 .data ["rows_count"])#line:387
            if (OO00OO0000OO00OO0 .upper ()=='FRSTPIM')|(OO00OO0000OO00OO0 .upper ()=='PIM1')|(OO00OO0000OO00OO0 .upper ()=='FRSTCONF')|(OO00OO0000OO00OO0 .upper ()=='CONF1'):#line:388
                OO0OO00O0OO00OO0O =OO0OO00O0OO00OO0O and (O0OO0O00OO00O0OO0 .quantifiers .get (OO00OO0000OO00OO0 )<=OO000OO0OOOO0OO0O )#line:389
            if (OO00OO0000OO00OO0 .upper ()=='SCNDPIM')|(OO00OO0000OO00OO0 .upper ()=='PIM2')|(OO00OO0000OO00OO0 .upper ()=='SCNDCONF')|(OO00OO0000OO00OO0 .upper ()=='CONF2'):#line:390
                OO0OO00O0OO00OO0O =OO0OO00O0OO00OO0O and (O0OO0O00OO00O0OO0 .quantifiers .get (OO00OO0000OO00OO0 )<=OOOO00OOOO0OOOOOO )#line:391
            if (OO00OO0000OO00OO0 .upper ()=='DELTAPIM')|(OO00OO0000OO00OO0 .upper ()=='DELTACONF'):#line:392
                OO0OO00O0OO00OO0O =OO0OO00O0OO00OO0O and (O0OO0O00OO00O0OO0 .quantifiers .get (OO00OO0000OO00OO0 )<=OO000OO0OOOO0OO0O -OOOO00OOOO0OOOOOO )#line:393
            if (OO00OO0000OO00OO0 .upper ()=='RATIOPIM')|(OO00OO0000OO00OO0 .upper ()=='RATIOCONF'):#line:396
                if (OOOO00OOOO0OOOOOO >0 ):#line:397
                    OO0OO00O0OO00OO0O =OO0OO00O0OO00OO0O and (O0OO0O00OO00O0OO0 .quantifiers .get (OO00OO0000OO00OO0 )<=OO000OO0OOOO0OO0O *1.0 /OOOO00OOOO0OOOOOO )#line:398
                else :#line:399
                    OO0OO00O0OO00OO0O =False #line:400
            if (OO00OO0000OO00OO0 .upper ()=='RATIOPIM_LEQ')|(OO00OO0000OO00OO0 .upper ()=='RATIOCONF_LEQ'):#line:401
                if (OOOO00OOOO0OOOOOO >0 ):#line:402
                    OO0OO00O0OO00OO0O =OO0OO00O0OO00OO0O and (O0OO0O00OO00O0OO0 .quantifiers .get (OO00OO0000OO00OO0 )>=OO000OO0OOOO0OO0O *1.0 /OOOO00OOOO0OOOOOO )#line:403
                else :#line:404
                    OO0OO00O0OO00OO0O =False #line:405
        OO0O00OO0000O00OO ={}#line:406
        if OO0OO00O0OO00OO0O ==True :#line:407
            O0OO0O00OO00O0OO0 .stats ['total_valid']+=1 #line:409
            OO0O00OO0000O00OO ["base1"]=O0OOO0OOO0OOO0OO0 #line:410
            OO0O00OO0000O00OO ["base2"]=OOO0O0OO0O00000O0 #line:411
            OO0O00OO0000O00OO ["rel_base1"]=O0OOO0OOO0OOO0OO0 *1.0 /O0OO0O00OO00O0OO0 .data ["rows_count"]#line:412
            OO0O00OO0000O00OO ["rel_base2"]=OOO0O0OO0O00000O0 *1.0 /O0OO0O00OO00O0OO0 .data ["rows_count"]#line:413
            OO0O00OO0000O00OO ["conf1"]=OO000OO0OOOO0OO0O #line:414
            OO0O00OO0000O00OO ["conf2"]=OOOO00OOOO0OOOOOO #line:415
            OO0O00OO0000O00OO ["deltaconf"]=OO000OO0OOOO0OO0O -OOOO00OOOO0OOOOOO #line:416
            if (OOOO00OOOO0OOOOOO >0 ):#line:417
                OO0O00OO0000O00OO ["ratioconf"]=OO000OO0OOOO0OO0O *1.0 /OOOO00OOOO0OOOOOO #line:418
            else :#line:419
                OO0O00OO0000O00OO ["ratioconf"]=None #line:420
            OO0O00OO0000O00OO ["fourfold1"]=[O0OOO0O00O00O0OOO ,O0OO00000OO00O000 ,O0OOOOO0O000OOOOO ,OOO0OO0O0OO0O000O ]#line:421
            OO0O00OO0000O00OO ["fourfold2"]=[OOO0O0OOO0O00OOO0 ,OOO0OOOO0OOO00OOO ,OOO000O0O0000O0O0 ,O0000OO0OOOO0O0O0 ]#line:422
        return OO0OO00O0OO00OO0O ,OO0O00OO0000O00OO #line:426
    def _verifynewact4ft (O000O00OOOO0O0OO0 ,_OO0OO0OOO0OOO0000 ):#line:428
        OO000OO00OO00O0OO ={}#line:429
        for OO00O000O0OO00O0O in O000O00OOOO0O0OO0 .task_actinfo ['cedents']:#line:430
            OO000OO00OO00O0OO [OO00O000O0OO00O0O ['cedent_type']]=OO00O000O0OO00O0O ['filter_value']#line:432
        OOO00O00OO00OOOOO =bin (OO000OO00OO00O0OO ['ante']&OO000OO00OO00O0OO ['succ']&OO000OO00OO00O0OO ['cond']).count ("1")#line:434
        OO0O0O00000OO00OO =bin (OO000OO00OO00O0OO ['ante']&OO000OO00OO00O0OO ['succ']&OO000OO00OO00O0OO ['cond']&OO000OO00OO00O0OO ['antv']&OO000OO00OO00O0OO ['sucv']).count ("1")#line:435
        OOOO0O00000O0OOO0 =None #line:436
        O0OOO000O000O0OO0 =0 #line:437
        O000000O0OOOOOO0O =0 #line:438
        if OOO00O00OO00OOOOO >0 :#line:447
            O0OOO000O000O0OO0 =bin (OO000OO00OO00O0OO ['ante']&OO000OO00OO00O0OO ['succ']&OO000OO00OO00O0OO ['cond']).count ("1")*1.0 /bin (OO000OO00OO00O0OO ['ante']&OO000OO00OO00O0OO ['cond']).count ("1")#line:449
        if OO0O0O00000OO00OO >0 :#line:450
            O000000O0OOOOOO0O =bin (OO000OO00OO00O0OO ['ante']&OO000OO00OO00O0OO ['succ']&OO000OO00OO00O0OO ['cond']&OO000OO00OO00O0OO ['antv']&OO000OO00OO00O0OO ['sucv']).count ("1")*1.0 /bin (OO000OO00OO00O0OO ['ante']&OO000OO00OO00O0OO ['cond']&OO000OO00OO00O0OO ['antv']).count ("1")#line:452
        OOO0OO0O0OOO00O0O =1 <<O000O00OOOO0O0OO0 .rows_count #line:454
        O0O0O0000OOO0O0OO =bin (OO000OO00OO00O0OO ['ante']&OO000OO00OO00O0OO ['succ']&OO000OO00OO00O0OO ['cond']).count ("1")#line:455
        OOOOO0OOOOO000OO0 =bin (OO000OO00OO00O0OO ['ante']&~(OOO0OO0O0OOO00O0O |OO000OO00OO00O0OO ['succ'])&OO000OO00OO00O0OO ['cond']).count ("1")#line:456
        O00OOO00OOOOOOOOO =bin (~(OOO0OO0O0OOO00O0O |OO000OO00OO00O0OO ['ante'])&OO000OO00OO00O0OO ['succ']&OO000OO00OO00O0OO ['cond']).count ("1")#line:457
        O0OO0000O00OOOOO0 =bin (~(OOO0OO0O0OOO00O0O |OO000OO00OO00O0OO ['ante'])&~(OOO0OO0O0OOO00O0O |OO000OO00OO00O0OO ['succ'])&OO000OO00OO00O0OO ['cond']).count ("1")#line:458
        OO000O00OO000OO0O =bin (OO000OO00OO00O0OO ['ante']&OO000OO00OO00O0OO ['succ']&OO000OO00OO00O0OO ['cond']&OO000OO00OO00O0OO ['antv']&OO000OO00OO00O0OO ['sucv']).count ("1")#line:459
        OO00O0O0OOOOOO0OO =bin (OO000OO00OO00O0OO ['ante']&~(OOO0OO0O0OOO00O0O |(OO000OO00OO00O0OO ['succ']&OO000OO00OO00O0OO ['sucv']))&OO000OO00OO00O0OO ['cond']).count ("1")#line:460
        O0O00O00OOO00O00O =bin (~(OOO0OO0O0OOO00O0O |(OO000OO00OO00O0OO ['ante']&OO000OO00OO00O0OO ['antv']))&OO000OO00OO00O0OO ['succ']&OO000OO00OO00O0OO ['cond']&OO000OO00OO00O0OO ['sucv']).count ("1")#line:461
        OOO0O0000O0000OOO =bin (~(OOO0OO0O0OOO00O0O |(OO000OO00OO00O0OO ['ante']&OO000OO00OO00O0OO ['antv']))&~(OOO0OO0O0OOO00O0O |(OO000OO00OO00O0OO ['succ']&OO000OO00OO00O0OO ['sucv']))&OO000OO00OO00O0OO ['cond']).count ("1")#line:462
        O0000O0OO00OO000O =True #line:463
        for OOOO0000000O0O00O in O000O00OOOO0O0OO0 .quantifiers .keys ():#line:464
            if (OOOO0000000O0O00O =='PreBase')|(OOOO0000000O0O00O =='Base1'):#line:465
                O0000O0OO00OO000O =O0000O0OO00OO000O and (O000O00OOOO0O0OO0 .quantifiers .get (OOOO0000000O0O00O )<=OOO00O00OO00OOOOO )#line:466
            if (OOOO0000000O0O00O =='PostBase')|(OOOO0000000O0O00O =='Base2'):#line:467
                O0000O0OO00OO000O =O0000O0OO00OO000O and (O000O00OOOO0O0OO0 .quantifiers .get (OOOO0000000O0O00O )<=OO0O0O00000OO00OO )#line:468
            if (OOOO0000000O0O00O =='PreRelBase')|(OOOO0000000O0O00O =='RelBase1'):#line:469
                O0000O0OO00OO000O =O0000O0OO00OO000O and (O000O00OOOO0O0OO0 .quantifiers .get (OOOO0000000O0O00O )<=OOO00O00OO00OOOOO *1.0 /O000O00OOOO0O0OO0 .data ["rows_count"])#line:470
            if (OOOO0000000O0O00O =='PostRelBase')|(OOOO0000000O0O00O =='RelBase2'):#line:471
                O0000O0OO00OO000O =O0000O0OO00OO000O and (O000O00OOOO0O0OO0 .quantifiers .get (OOOO0000000O0O00O )<=OO0O0O00000OO00OO *1.0 /O000O00OOOO0O0OO0 .data ["rows_count"])#line:472
            if (OOOO0000000O0O00O =='Prepim')|(OOOO0000000O0O00O =='pim1')|(OOOO0000000O0O00O =='PreConf')|(OOOO0000000O0O00O =='conf1'):#line:473
                O0000O0OO00OO000O =O0000O0OO00OO000O and (O000O00OOOO0O0OO0 .quantifiers .get (OOOO0000000O0O00O )<=O0OOO000O000O0OO0 )#line:474
            if (OOOO0000000O0O00O =='Postpim')|(OOOO0000000O0O00O =='pim2')|(OOOO0000000O0O00O =='PostConf')|(OOOO0000000O0O00O =='conf2'):#line:475
                O0000O0OO00OO000O =O0000O0OO00OO000O and (O000O00OOOO0O0OO0 .quantifiers .get (OOOO0000000O0O00O )<=O000000O0OOOOOO0O )#line:476
            if (OOOO0000000O0O00O =='Deltapim')|(OOOO0000000O0O00O =='DeltaConf'):#line:477
                O0000O0OO00OO000O =O0000O0OO00OO000O and (O000O00OOOO0O0OO0 .quantifiers .get (OOOO0000000O0O00O )<=O0OOO000O000O0OO0 -O000000O0OOOOOO0O )#line:478
            if (OOOO0000000O0O00O =='Ratiopim')|(OOOO0000000O0O00O =='RatioConf'):#line:481
                if (O000000O0OOOOOO0O >0 ):#line:482
                    O0000O0OO00OO000O =O0000O0OO00OO000O and (O000O00OOOO0O0OO0 .quantifiers .get (OOOO0000000O0O00O )<=O0OOO000O000O0OO0 *1.0 /O000000O0OOOOOO0O )#line:483
                else :#line:484
                    O0000O0OO00OO000O =False #line:485
        O0O000O00O000OO00 ={}#line:486
        if O0000O0OO00OO000O ==True :#line:487
            O000O00OOOO0O0OO0 .stats ['total_valid']+=1 #line:489
            O0O000O00O000OO00 ["base1"]=OOO00O00OO00OOOOO #line:490
            O0O000O00O000OO00 ["base2"]=OO0O0O00000OO00OO #line:491
            O0O000O00O000OO00 ["rel_base1"]=OOO00O00OO00OOOOO *1.0 /O000O00OOOO0O0OO0 .data ["rows_count"]#line:492
            O0O000O00O000OO00 ["rel_base2"]=OO0O0O00000OO00OO *1.0 /O000O00OOOO0O0OO0 .data ["rows_count"]#line:493
            O0O000O00O000OO00 ["conf1"]=O0OOO000O000O0OO0 #line:494
            O0O000O00O000OO00 ["conf2"]=O000000O0OOOOOO0O #line:495
            O0O000O00O000OO00 ["deltaconf"]=O0OOO000O000O0OO0 -O000000O0OOOOOO0O #line:496
            if (O000000O0OOOOOO0O >0 ):#line:497
                O0O000O00O000OO00 ["ratioconf"]=O0OOO000O000O0OO0 *1.0 /O000000O0OOOOOO0O #line:498
            else :#line:499
                O0O000O00O000OO00 ["ratioconf"]=None #line:500
            O0O000O00O000OO00 ["fourfoldpre"]=[O0O0O0000OOO0O0OO ,OOOOO0OOOOO000OO0 ,O00OOO00OOOOOOOOO ,O0OO0000O00OOOOO0 ]#line:501
            O0O000O00O000OO00 ["fourfoldpost"]=[OO000O00OO000OO0O ,OO00O0O0OOOOOO0OO ,O0O00O00OOO00O00O ,OOO0O0000O0000OOO ]#line:502
        return O0000O0OO00OO000O ,O0O000O00O000OO00 #line:504
    def _verifyact4ft (O00O00000O0O00OO0 ,_OOO0000O0OO0000O0 ):#line:506
        OO00OO0OO00OO0O0O ={}#line:507
        for OOOO0OOOO0OO0O0O0 in O00O00000O0O00OO0 .task_actinfo ['cedents']:#line:508
            OO00OO0OO00OO0O0O [OOOO0OOOO0OO0O0O0 ['cedent_type']]=OOOO0OOOO0OO0O0O0 ['filter_value']#line:510
        O0O0OO000000OOOO0 =bin (OO00OO0OO00OO0O0O ['ante']&OO00OO0OO00OO0O0O ['succ']&OO00OO0OO00OO0O0O ['cond']&OO00OO0OO00OO0O0O ['antv-']&OO00OO0OO00OO0O0O ['sucv-']).count ("1")#line:512
        O0O0OOOO0000OO0O0 =bin (OO00OO0OO00OO0O0O ['ante']&OO00OO0OO00OO0O0O ['succ']&OO00OO0OO00OO0O0O ['cond']&OO00OO0OO00OO0O0O ['antv+']&OO00OO0OO00OO0O0O ['sucv+']).count ("1")#line:513
        O0O0000O00O0000O0 =None #line:514
        OOO0000OO000O0OO0 =0 #line:515
        O000O0OO0OOO00000 =0 #line:516
        if O0O0OO000000OOOO0 >0 :#line:525
            OOO0000OO000O0OO0 =bin (OO00OO0OO00OO0O0O ['ante']&OO00OO0OO00OO0O0O ['succ']&OO00OO0OO00OO0O0O ['cond']&OO00OO0OO00OO0O0O ['antv-']&OO00OO0OO00OO0O0O ['sucv-']).count ("1")*1.0 /bin (OO00OO0OO00OO0O0O ['ante']&OO00OO0OO00OO0O0O ['cond']&OO00OO0OO00OO0O0O ['antv-']).count ("1")#line:527
        if O0O0OOOO0000OO0O0 >0 :#line:528
            O000O0OO0OOO00000 =bin (OO00OO0OO00OO0O0O ['ante']&OO00OO0OO00OO0O0O ['succ']&OO00OO0OO00OO0O0O ['cond']&OO00OO0OO00OO0O0O ['antv+']&OO00OO0OO00OO0O0O ['sucv+']).count ("1")*1.0 /bin (OO00OO0OO00OO0O0O ['ante']&OO00OO0OO00OO0O0O ['cond']&OO00OO0OO00OO0O0O ['antv+']).count ("1")#line:530
        O0OOOO00O000OOOOO =1 <<O00O00000O0O00OO0 .data ["rows_count"]#line:532
        O00OOOOO0O0OO0O0O =bin (OO00OO0OO00OO0O0O ['ante']&OO00OO0OO00OO0O0O ['succ']&OO00OO0OO00OO0O0O ['cond']&OO00OO0OO00OO0O0O ['antv-']&OO00OO0OO00OO0O0O ['sucv-']).count ("1")#line:533
        O00OOOOO0O00O0O0O =bin (OO00OO0OO00OO0O0O ['ante']&OO00OO0OO00OO0O0O ['antv-']&~(O0OOOO00O000OOOOO |(OO00OO0OO00OO0O0O ['succ']&OO00OO0OO00OO0O0O ['sucv-']))&OO00OO0OO00OO0O0O ['cond']).count ("1")#line:534
        OO0O00OO0OO00O0O0 =bin (~(O0OOOO00O000OOOOO |(OO00OO0OO00OO0O0O ['ante']&OO00OO0OO00OO0O0O ['antv-']))&OO00OO0OO00OO0O0O ['succ']&OO00OO0OO00OO0O0O ['cond']&OO00OO0OO00OO0O0O ['sucv-']).count ("1")#line:535
        O0O0000O0O0O0O00O =bin (~(O0OOOO00O000OOOOO |(OO00OO0OO00OO0O0O ['ante']&OO00OO0OO00OO0O0O ['antv-']))&~(O0OOOO00O000OOOOO |(OO00OO0OO00OO0O0O ['succ']&OO00OO0OO00OO0O0O ['sucv-']))&OO00OO0OO00OO0O0O ['cond']).count ("1")#line:536
        OO0OOO0O0O0OOOO0O =bin (OO00OO0OO00OO0O0O ['ante']&OO00OO0OO00OO0O0O ['succ']&OO00OO0OO00OO0O0O ['cond']&OO00OO0OO00OO0O0O ['antv+']&OO00OO0OO00OO0O0O ['sucv+']).count ("1")#line:537
        O0OO0O0OOOO00O0O0 =bin (OO00OO0OO00OO0O0O ['ante']&OO00OO0OO00OO0O0O ['antv+']&~(O0OOOO00O000OOOOO |(OO00OO0OO00OO0O0O ['succ']&OO00OO0OO00OO0O0O ['sucv+']))&OO00OO0OO00OO0O0O ['cond']).count ("1")#line:538
        OO000O00000O00000 =bin (~(O0OOOO00O000OOOOO |(OO00OO0OO00OO0O0O ['ante']&OO00OO0OO00OO0O0O ['antv+']))&OO00OO0OO00OO0O0O ['succ']&OO00OO0OO00OO0O0O ['cond']&OO00OO0OO00OO0O0O ['sucv+']).count ("1")#line:539
        OO00O00O0O0O0O0OO =bin (~(O0OOOO00O000OOOOO |(OO00OO0OO00OO0O0O ['ante']&OO00OO0OO00OO0O0O ['antv+']))&~(O0OOOO00O000OOOOO |(OO00OO0OO00OO0O0O ['succ']&OO00OO0OO00OO0O0O ['sucv+']))&OO00OO0OO00OO0O0O ['cond']).count ("1")#line:540
        OOO00OO000OOOOO00 =True #line:541
        for O0OO000OOO0O0O000 in O00O00000O0O00OO0 .quantifiers .keys ():#line:542
            if (O0OO000OOO0O0O000 =='PreBase')|(O0OO000OOO0O0O000 =='Base1'):#line:543
                OOO00OO000OOOOO00 =OOO00OO000OOOOO00 and (O00O00000O0O00OO0 .quantifiers .get (O0OO000OOO0O0O000 )<=O0O0OO000000OOOO0 )#line:544
            if (O0OO000OOO0O0O000 =='PostBase')|(O0OO000OOO0O0O000 =='Base2'):#line:545
                OOO00OO000OOOOO00 =OOO00OO000OOOOO00 and (O00O00000O0O00OO0 .quantifiers .get (O0OO000OOO0O0O000 )<=O0O0OOOO0000OO0O0 )#line:546
            if (O0OO000OOO0O0O000 =='PreRelBase')|(O0OO000OOO0O0O000 =='RelBase1'):#line:547
                OOO00OO000OOOOO00 =OOO00OO000OOOOO00 and (O00O00000O0O00OO0 .quantifiers .get (O0OO000OOO0O0O000 )<=O0O0OO000000OOOO0 *1.0 /O00O00000O0O00OO0 .data ["rows_count"])#line:548
            if (O0OO000OOO0O0O000 =='PostRelBase')|(O0OO000OOO0O0O000 =='RelBase2'):#line:549
                OOO00OO000OOOOO00 =OOO00OO000OOOOO00 and (O00O00000O0O00OO0 .quantifiers .get (O0OO000OOO0O0O000 )<=O0O0OOOO0000OO0O0 *1.0 /O00O00000O0O00OO0 .data ["rows_count"])#line:550
            if (O0OO000OOO0O0O000 =='Prepim')|(O0OO000OOO0O0O000 =='pim1')|(O0OO000OOO0O0O000 =='PreConf')|(O0OO000OOO0O0O000 =='conf1'):#line:551
                OOO00OO000OOOOO00 =OOO00OO000OOOOO00 and (O00O00000O0O00OO0 .quantifiers .get (O0OO000OOO0O0O000 )<=OOO0000OO000O0OO0 )#line:552
            if (O0OO000OOO0O0O000 =='Postpim')|(O0OO000OOO0O0O000 =='pim2')|(O0OO000OOO0O0O000 =='PostConf')|(O0OO000OOO0O0O000 =='conf2'):#line:553
                OOO00OO000OOOOO00 =OOO00OO000OOOOO00 and (O00O00000O0O00OO0 .quantifiers .get (O0OO000OOO0O0O000 )<=O000O0OO0OOO00000 )#line:554
            if (O0OO000OOO0O0O000 =='Deltapim')|(O0OO000OOO0O0O000 =='DeltaConf'):#line:555
                OOO00OO000OOOOO00 =OOO00OO000OOOOO00 and (O00O00000O0O00OO0 .quantifiers .get (O0OO000OOO0O0O000 )<=OOO0000OO000O0OO0 -O000O0OO0OOO00000 )#line:556
            if (O0OO000OOO0O0O000 =='Ratiopim')|(O0OO000OOO0O0O000 =='RatioConf'):#line:559
                if (OOO0000OO000O0OO0 >0 ):#line:560
                    OOO00OO000OOOOO00 =OOO00OO000OOOOO00 and (O00O00000O0O00OO0 .quantifiers .get (O0OO000OOO0O0O000 )<=O000O0OO0OOO00000 *1.0 /OOO0000OO000O0OO0 )#line:561
                else :#line:562
                    OOO00OO000OOOOO00 =False #line:563
        OOOOO0O00O0OO0OOO ={}#line:564
        if OOO00OO000OOOOO00 ==True :#line:565
            O00O00000O0O00OO0 .stats ['total_valid']+=1 #line:567
            OOOOO0O00O0OO0OOO ["base1"]=O0O0OO000000OOOO0 #line:568
            OOOOO0O00O0OO0OOO ["base2"]=O0O0OOOO0000OO0O0 #line:569
            OOOOO0O00O0OO0OOO ["rel_base1"]=O0O0OO000000OOOO0 *1.0 /O00O00000O0O00OO0 .data ["rows_count"]#line:570
            OOOOO0O00O0OO0OOO ["rel_base2"]=O0O0OOOO0000OO0O0 *1.0 /O00O00000O0O00OO0 .data ["rows_count"]#line:571
            OOOOO0O00O0OO0OOO ["conf1"]=OOO0000OO000O0OO0 #line:572
            OOOOO0O00O0OO0OOO ["conf2"]=O000O0OO0OOO00000 #line:573
            OOOOO0O00O0OO0OOO ["deltaconf"]=OOO0000OO000O0OO0 -O000O0OO0OOO00000 #line:574
            if (OOO0000OO000O0OO0 >0 ):#line:575
                OOOOO0O00O0OO0OOO ["ratioconf"]=O000O0OO0OOO00000 *1.0 /OOO0000OO000O0OO0 #line:576
            else :#line:577
                OOOOO0O00O0OO0OOO ["ratioconf"]=None #line:578
            OOOOO0O00O0OO0OOO ["fourfoldpre"]=[O00OOOOO0O0OO0O0O ,O00OOOOO0O00O0O0O ,OO0O00OO0OO00O0O0 ,O0O0000O0O0O0O00O ]#line:579
            OOOOO0O00O0OO0OOO ["fourfoldpost"]=[OO0OOO0O0O0OOOO0O ,O0OO0O0OOOO00O0O0 ,OO000O00000O00000 ,OO00O00O0O0O0O0OO ]#line:580
        return OOO00OO000OOOOO00 ,OOOOO0O00O0OO0OOO #line:582
    def _verify_opt (O0OO0O00OOOOO000O ,O0O000000O0000000 ,O0OOO0OO0OO0OOO00 ):#line:584
        O00OOO0O0OO0OO0O0 =False #line:585
        if not (O0O000000O0000000 ['optim'].get ('only_con')):#line:588
            return False #line:589
        OO0O0OOO000O0OOOO ={}#line:590
        for O0OO0OO0O0OOOOO00 in O0OO0O00OOOOO000O .task_actinfo ['cedents']:#line:591
            OO0O0OOO000O0OOOO [O0OO0OO0O0OOOOO00 ['cedent_type']]=O0OO0OO0O0OOOOO00 ['filter_value']#line:593
        O00000OO00O00OOOO =1 <<O0OO0O00OOOOO000O .data ["rows_count"]#line:595
        O00000O000OO00O0O =O00000OO00O00OOOO -1 #line:596
        O0O0O000000OO0O0O =""#line:597
        OOOOOO00000000O0O =0 #line:598
        if (OO0O0OOO000O0OOOO .get ('ante')!=None ):#line:599
            O00000O000OO00O0O =O00000O000OO00O0O &OO0O0OOO000O0OOOO ['ante']#line:600
        if (OO0O0OOO000O0OOOO .get ('succ')!=None ):#line:601
            O00000O000OO00O0O =O00000O000OO00O0O &OO0O0OOO000O0OOOO ['succ']#line:602
        if (OO0O0OOO000O0OOOO .get ('cond')!=None ):#line:603
            O00000O000OO00O0O =O00000O000OO00O0O &OO0O0OOO000O0OOOO ['cond']#line:604
        O000O000O0O0OOOOO =None #line:607
        if (O0OO0O00OOOOO000O .proc =='CFMiner')|(O0OO0O00OOOOO000O .proc =='4ftMiner'):#line:632
            OO00O000000OOOO0O =bin (O00000O000OO00O0O ).count ("1")#line:633
            for OOOOOOOO000O00OOO in O0OO0O00OOOOO000O .quantifiers .keys ():#line:634
                if OOOOOOOO000O00OOO =='Base':#line:635
                    if not (O0OO0O00OOOOO000O .quantifiers .get (OOOOOOOO000O00OOO )<=OO00O000000OOOO0O ):#line:636
                        O00OOO0O0OO0OO0O0 =True #line:637
                if OOOOOOOO000O00OOO =='RelBase':#line:639
                    if not (O0OO0O00OOOOO000O .quantifiers .get (OOOOOOOO000O00OOO )<=OO00O000000OOOO0O *1.0 /O0OO0O00OOOOO000O .data ["rows_count"]):#line:640
                        O00OOO0O0OO0OO0O0 =True #line:641
        return O00OOO0O0OO0OO0O0 #line:644
        if O0OO0O00OOOOO000O .proc =='CFMiner':#line:647
            if (O0OOO0OO0OO0OOO00 ['cedent_type']=='cond')&(O0OOO0OO0OO0OOO00 ['defi'].get ('type')=='con'):#line:648
                OO00O000000OOOO0O =bin (OO0O0OOO000O0OOOO ['cond']).count ("1")#line:649
                OO0O00O0OO0OO0OO0 =True #line:650
                for OOOOOOOO000O00OOO in O0OO0O00OOOOO000O .quantifiers .keys ():#line:651
                    if OOOOOOOO000O00OOO =='Base':#line:652
                        OO0O00O0OO0OO0OO0 =OO0O00O0OO0OO0OO0 and (O0OO0O00OOOOO000O .quantifiers .get (OOOOOOOO000O00OOO )<=OO00O000000OOOO0O )#line:653
                        if not (OO0O00O0OO0OO0OO0 ):#line:654
                            print (f"...optimization : base is {OO00O000000OOOO0O} for {O0OOO0OO0OO0OOO00['generated_string']}")#line:655
                    if OOOOOOOO000O00OOO =='RelBase':#line:656
                        OO0O00O0OO0OO0OO0 =OO0O00O0OO0OO0OO0 and (O0OO0O00OOOOO000O .quantifiers .get (OOOOOOOO000O00OOO )<=OO00O000000OOOO0O *1.0 /O0OO0O00OOOOO000O .data ["rows_count"])#line:657
                        if not (OO0O00O0OO0OO0OO0 ):#line:658
                            print (f"...optimization : base is {OO00O000000OOOO0O} for {O0OOO0OO0OO0OOO00['generated_string']}")#line:659
                O00OOO0O0OO0OO0O0 =not (OO0O00O0OO0OO0OO0 )#line:660
        elif O0OO0O00OOOOO000O .proc =='4ftMiner':#line:661
            if (O0OOO0OO0OO0OOO00 ['cedent_type']=='cond')&(O0OOO0OO0OO0OOO00 ['defi'].get ('type')=='con'):#line:662
                OO00O000000OOOO0O =bin (OO0O0OOO000O0OOOO ['cond']).count ("1")#line:663
                OO0O00O0OO0OO0OO0 =True #line:664
                for OOOOOOOO000O00OOO in O0OO0O00OOOOO000O .quantifiers .keys ():#line:665
                    if OOOOOOOO000O00OOO =='Base':#line:666
                        OO0O00O0OO0OO0OO0 =OO0O00O0OO0OO0OO0 and (O0OO0O00OOOOO000O .quantifiers .get (OOOOOOOO000O00OOO )<=OO00O000000OOOO0O )#line:667
                        if not (OO0O00O0OO0OO0OO0 ):#line:668
                            print (f"...optimization : base is {OO00O000000OOOO0O} for {O0OOO0OO0OO0OOO00['generated_string']}")#line:669
                    if OOOOOOOO000O00OOO =='RelBase':#line:670
                        OO0O00O0OO0OO0OO0 =OO0O00O0OO0OO0OO0 and (O0OO0O00OOOOO000O .quantifiers .get (OOOOOOOO000O00OOO )<=OO00O000000OOOO0O *1.0 /O0OO0O00OOOOO000O .data ["rows_count"])#line:671
                        if not (OO0O00O0OO0OO0OO0 ):#line:672
                            print (f"...optimization : base is {OO00O000000OOOO0O} for {O0OOO0OO0OO0OOO00['generated_string']}")#line:673
                O00OOO0O0OO0OO0O0 =not (OO0O00O0OO0OO0OO0 )#line:674
            if (O0OOO0OO0OO0OOO00 ['cedent_type']=='ante')&(O0OOO0OO0OO0OOO00 ['defi'].get ('type')=='con'):#line:675
                OO00O000000OOOO0O =bin (OO0O0OOO000O0OOOO ['ante']&OO0O0OOO000O0OOOO ['cond']).count ("1")#line:676
                OO0O00O0OO0OO0OO0 =True #line:677
                for OOOOOOOO000O00OOO in O0OO0O00OOOOO000O .quantifiers .keys ():#line:678
                    if OOOOOOOO000O00OOO =='Base':#line:679
                        OO0O00O0OO0OO0OO0 =OO0O00O0OO0OO0OO0 and (O0OO0O00OOOOO000O .quantifiers .get (OOOOOOOO000O00OOO )<=OO00O000000OOOO0O )#line:680
                        if not (OO0O00O0OO0OO0OO0 ):#line:681
                            print (f"...optimization : ANTE: base is {OO00O000000OOOO0O} for {O0OOO0OO0OO0OOO00['generated_string']}")#line:682
                    if OOOOOOOO000O00OOO =='RelBase':#line:683
                        OO0O00O0OO0OO0OO0 =OO0O00O0OO0OO0OO0 and (O0OO0O00OOOOO000O .quantifiers .get (OOOOOOOO000O00OOO )<=OO00O000000OOOO0O *1.0 /O0OO0O00OOOOO000O .data ["rows_count"])#line:684
                        if not (OO0O00O0OO0OO0OO0 ):#line:685
                            print (f"...optimization : ANTE:  base is {OO00O000000OOOO0O} for {O0OOO0OO0OO0OOO00['generated_string']}")#line:686
                O00OOO0O0OO0OO0O0 =not (OO0O00O0OO0OO0OO0 )#line:687
            if (O0OOO0OO0OO0OOO00 ['cedent_type']=='succ')&(O0OOO0OO0OO0OOO00 ['defi'].get ('type')=='con'):#line:688
                OO00O000000OOOO0O =bin (OO0O0OOO000O0OOOO ['ante']&OO0O0OOO000O0OOOO ['cond']&OO0O0OOO000O0OOOO ['succ']).count ("1")#line:689
                O000O000O0O0OOOOO =0 #line:690
                if OO00O000000OOOO0O >0 :#line:691
                    O000O000O0O0OOOOO =bin (OO0O0OOO000O0OOOO ['ante']&OO0O0OOO000O0OOOO ['succ']&OO0O0OOO000O0OOOO ['cond']).count ("1")*1.0 /bin (OO0O0OOO000O0OOOO ['ante']&OO0O0OOO000O0OOOO ['cond']).count ("1")#line:692
                O00000OO00O00OOOO =1 <<O0OO0O00OOOOO000O .data ["rows_count"]#line:693
                O0OO0OO0000OOO0O0 =bin (OO0O0OOO000O0OOOO ['ante']&OO0O0OOO000O0OOOO ['succ']&OO0O0OOO000O0OOOO ['cond']).count ("1")#line:694
                OOO00OO00OOO00OO0 =bin (OO0O0OOO000O0OOOO ['ante']&~(O00000OO00O00OOOO |OO0O0OOO000O0OOOO ['succ'])&OO0O0OOO000O0OOOO ['cond']).count ("1")#line:695
                O0OO0OO0O0OOOOO00 =bin (~(O00000OO00O00OOOO |OO0O0OOO000O0OOOO ['ante'])&OO0O0OOO000O0OOOO ['succ']&OO0O0OOO000O0OOOO ['cond']).count ("1")#line:696
                O0OO0O00O00000OO0 =bin (~(O00000OO00O00OOOO |OO0O0OOO000O0OOOO ['ante'])&~(O00000OO00O00OOOO |OO0O0OOO000O0OOOO ['succ'])&OO0O0OOO000O0OOOO ['cond']).count ("1")#line:697
                OO0O00O0OO0OO0OO0 =True #line:698
                for OOOOOOOO000O00OOO in O0OO0O00OOOOO000O .quantifiers .keys ():#line:699
                    if OOOOOOOO000O00OOO =='pim':#line:700
                        OO0O00O0OO0OO0OO0 =OO0O00O0OO0OO0OO0 and (O0OO0O00OOOOO000O .quantifiers .get (OOOOOOOO000O00OOO )<=O000O000O0O0OOOOO )#line:701
                    if not (OO0O00O0OO0OO0OO0 ):#line:702
                        print (f"...optimization : SUCC:  pim is {O000O000O0O0OOOOO} for {O0OOO0OO0OO0OOO00['generated_string']}")#line:703
                    if OOOOOOOO000O00OOO =='aad':#line:705
                        if (O0OO0OO0000OOO0O0 +OOO00OO00OOO00OO0 )*(O0OO0OO0000OOO0O0 +O0OO0OO0O0OOOOO00 )>0 :#line:706
                            OO0O00O0OO0OO0OO0 =OO0O00O0OO0OO0OO0 and (O0OO0O00OOOOO000O .quantifiers .get (OOOOOOOO000O00OOO )<=O0OO0OO0000OOO0O0 *(O0OO0OO0000OOO0O0 +OOO00OO00OOO00OO0 +O0OO0OO0O0OOOOO00 +O0OO0O00O00000OO0 )/(O0OO0OO0000OOO0O0 +OOO00OO00OOO00OO0 )/(O0OO0OO0000OOO0O0 +O0OO0OO0O0OOOOO00 )-1 )#line:707
                        else :#line:708
                            OO0O00O0OO0OO0OO0 =False #line:709
                        if not (OO0O00O0OO0OO0OO0 ):#line:710
                            O00O000O00O000000 =O0OO0OO0000OOO0O0 *(O0OO0OO0000OOO0O0 +OOO00OO00OOO00OO0 +O0OO0OO0O0OOOOO00 +O0OO0O00O00000OO0 )/(O0OO0OO0000OOO0O0 +OOO00OO00OOO00OO0 )/(O0OO0OO0000OOO0O0 +O0OO0OO0O0OOOOO00 )-1 #line:711
                            print (f"...optimization : SUCC:  aad is {O00O000O00O000000} for {O0OOO0OO0OO0OOO00['generated_string']}")#line:712
                    if OOOOOOOO000O00OOO =='bad':#line:713
                        if (O0OO0OO0000OOO0O0 +OOO00OO00OOO00OO0 )*(O0OO0OO0000OOO0O0 +O0OO0OO0O0OOOOO00 )>0 :#line:714
                            OO0O00O0OO0OO0OO0 =OO0O00O0OO0OO0OO0 and (O0OO0O00OOOOO000O .quantifiers .get (OOOOOOOO000O00OOO )<=1 -O0OO0OO0000OOO0O0 *(O0OO0OO0000OOO0O0 +OOO00OO00OOO00OO0 +O0OO0OO0O0OOOOO00 +O0OO0O00O00000OO0 )/(O0OO0OO0000OOO0O0 +OOO00OO00OOO00OO0 )/(O0OO0OO0000OOO0O0 +O0OO0OO0O0OOOOO00 ))#line:715
                        else :#line:716
                            OO0O00O0OO0OO0OO0 =False #line:717
                        if not (OO0O00O0OO0OO0OO0 ):#line:718
                            OOO0OO0O0O0OO0OOO =1 -O0OO0OO0000OOO0O0 *(O0OO0OO0000OOO0O0 +OOO00OO00OOO00OO0 +O0OO0OO0O0OOOOO00 +O0OO0O00O00000OO0 )/(O0OO0OO0000OOO0O0 +OOO00OO00OOO00OO0 )/(O0OO0OO0000OOO0O0 +O0OO0OO0O0OOOOO00 )#line:719
                            print (f"...optimization : SUCC:  bad is {OOO0OO0O0O0OO0OOO} for {O0OOO0OO0OO0OOO00['generated_string']}")#line:720
                O00OOO0O0OO0OO0O0 =not (OO0O00O0OO0OO0OO0 )#line:721
        if (O00OOO0O0OO0OO0O0 ):#line:722
            print (f"... OPTIMALIZATION - SKIPPING BRANCH at cedent {O0OOO0OO0OO0OOO00['cedent_type']}")#line:723
        return O00OOO0O0OO0OO0O0 #line:724
    def _print (O00000000000O00OO ,OO000O0O0OOO0O000 ,_O000O0O00OO00O00O ,_OO0OO0000O00O0000 ):#line:727
        if (len (_O000O0O00OO00O00O ))!=len (_OO0OO0000O00O0000 ):#line:728
            print ("DIFF IN LEN for following cedent : "+str (len (_O000O0O00OO00O00O ))+" vs "+str (len (_OO0OO0000O00O0000 )))#line:729
            print ("trace cedent : "+str (_O000O0O00OO00O00O )+", traces "+str (_OO0OO0000O00O0000 ))#line:730
        O0OOO0O00OO00O00O =''#line:731
        for O00000O0000000O00 in range (len (_O000O0O00OO00O00O )):#line:732
            O0O0O0O0OOOO0O0O0 =O00000000000O00OO .data ["varname"].index (OO000O0O0OOO0O000 ['defi'].get ('attributes')[_O000O0O00OO00O00O [O00000O0000000O00 ]].get ('name'))#line:733
            O0OOO0O00OO00O00O =O0OOO0O00OO00O00O +O00000000000O00OO .data ["varname"][O0O0O0O0OOOO0O0O0 ]+'('#line:735
            for OOOOO0OO00O0000O0 in _OO0OO0000O00O0000 [O00000O0000000O00 ]:#line:736
                O0OOO0O00OO00O00O =O0OOO0O00OO00O00O +str (O00000000000O00OO .data ["catnames"][O0O0O0O0OOOO0O0O0 ][OOOOO0OO00O0000O0 ])+" "#line:737
            O0OOO0O00OO00O00O =O0OOO0O00OO00O00O +')'#line:738
            if O00000O0000000O00 +1 <len (_O000O0O00OO00O00O ):#line:739
                O0OOO0O00OO00O00O =O0OOO0O00OO00O00O +' & '#line:740
        return O0OOO0O00OO00O00O #line:744
    def _print_hypo (OO0O000O0OOOO0000 ,OOO00O00O00OOOOO0 ):#line:746
        OO0O000O0OOOO0000 .print_rule (OOO00O00O00OOOOO0 )#line:747
    def _print_rule (OOOO000OOOOO000OO ,OOO0000OO00OO0000 ):#line:749
        print ('Rules info : '+str (OOO0000OO00OO0000 ['params']))#line:750
        for OO0O0O000O00O0OO0 in OOOO000OOOOO000OO .task_actinfo ['cedents']:#line:751
            print (OO0O0O000O00O0OO0 ['cedent_type']+' = '+OO0O0O000O00O0OO0 ['generated_string'])#line:752
    def _genvar (O0O0OOO0OOOOO00OO ,O0OO00O0O0OOO0OO0 ,O00000O0O0O0000OO ,_O00O000OO00OOOO00 ,_OO00O00000OOOOO00 ,_O0OO0O00OOOOO0O00 ,_OO0OOO00OO00OOOOO ,_O00O00OOOOO00OO0O ):#line:754
        for O00O0OOOOOOO00000 in range (O00000O0O0O0000OO ['num_cedent']):#line:755
            if len (_O00O000OO00OOOO00 )==0 or O00O0OOOOOOO00000 >_O00O000OO00OOOO00 [-1 ]:#line:756
                _O00O000OO00OOOO00 .append (O00O0OOOOOOO00000 )#line:757
                OOO00OO0O0O000OO0 =O0O0OOO0OOOOO00OO .data ["varname"].index (O00000O0O0O0000OO ['defi'].get ('attributes')[O00O0OOOOOOO00000 ].get ('name'))#line:758
                _O0O0OOO0000O0OOO0 =O00000O0O0O0000OO ['defi'].get ('attributes')[O00O0OOOOOOO00000 ].get ('minlen')#line:759
                _O0O000O000000OOOO =O00000O0O0O0000OO ['defi'].get ('attributes')[O00O0OOOOOOO00000 ].get ('maxlen')#line:760
                _O0000OO0O00OO0000 =O00000O0O0O0000OO ['defi'].get ('attributes')[O00O0OOOOOOO00000 ].get ('type')#line:761
                O0OOOOOO0OOOO0O0O =len (O0O0OOO0OOOOO00OO .data ["dm"][OOO00OO0O0O000OO0 ])#line:762
                _O0O0O000O0O00OOO0 =[]#line:763
                _OO00O00000OOOOO00 .append (_O0O0O000O0O00OOO0 )#line:764
                _OOO000O0O0000OO0O =int (0 )#line:765
                O0O0OOO0OOOOO00OO ._gencomb (O0OO00O0O0OOO0OO0 ,O00000O0O0O0000OO ,_O00O000OO00OOOO00 ,_OO00O00000OOOOO00 ,_O0O0O000O0O00OOO0 ,_O0OO0O00OOOOO0O00 ,_OOO000O0O0000OO0O ,O0OOOOOO0OOOO0O0O ,_O0000OO0O00OO0000 ,_OO0OOO00OO00OOOOO ,_O00O00OOOOO00OO0O ,_O0O0OOO0000O0OOO0 ,_O0O000O000000OOOO )#line:766
                _OO00O00000OOOOO00 .pop ()#line:767
                _O00O000OO00OOOO00 .pop ()#line:768
    def _gencomb (OOOO0O00O0000O0OO ,OO0O00O0OO0000000 ,OOOOO00OO0O0O0000 ,_O00000OO0000O00OO ,_O000000O000O000O0 ,_OO00OO00OOOO0O0OO ,_OOOO0OOOO00O00O00 ,_O00OO0OOOOOO0000O ,O00000O00OOO0OOOO ,_O00OO000000O00OO0 ,_OO000O0OO0O0OO00O ,_OOOO0O00O00O0O000 ,_O0OO00OO0O0OOO000 ,_OO000O000OO0OO0OO ):#line:770
        _O0O0OOOOO0000000O =[]#line:771
        if _O00OO000000O00OO0 =="subset":#line:772
            if len (_OO00OO00OOOO0O0OO )==0 :#line:773
                _O0O0OOOOO0000000O =range (O00000O00OOO0OOOO )#line:774
            else :#line:775
                _O0O0OOOOO0000000O =range (_OO00OO00OOOO0O0OO [-1 ]+1 ,O00000O00OOO0OOOO )#line:776
        elif _O00OO000000O00OO0 =="seq":#line:777
            if len (_OO00OO00OOOO0O0OO )==0 :#line:778
                _O0O0OOOOO0000000O =range (O00000O00OOO0OOOO -_O0OO00OO0O0OOO000 +1 )#line:779
            else :#line:780
                if _OO00OO00OOOO0O0OO [-1 ]+1 ==O00000O00OOO0OOOO :#line:781
                    return #line:782
                OOOOO0OOO000O00O0 =_OO00OO00OOOO0O0OO [-1 ]+1 #line:783
                _O0O0OOOOO0000000O .append (OOOOO0OOO000O00O0 )#line:784
        elif _O00OO000000O00OO0 =="lcut":#line:785
            if len (_OO00OO00OOOO0O0OO )==0 :#line:786
                OOOOO0OOO000O00O0 =0 ;#line:787
            else :#line:788
                if _OO00OO00OOOO0O0OO [-1 ]+1 ==O00000O00OOO0OOOO :#line:789
                    return #line:790
                OOOOO0OOO000O00O0 =_OO00OO00OOOO0O0OO [-1 ]+1 #line:791
            _O0O0OOOOO0000000O .append (OOOOO0OOO000O00O0 )#line:792
        elif _O00OO000000O00OO0 =="rcut":#line:793
            if len (_OO00OO00OOOO0O0OO )==0 :#line:794
                OOOOO0OOO000O00O0 =O00000O00OOO0OOOO -1 ;#line:795
            else :#line:796
                if _OO00OO00OOOO0O0OO [-1 ]==0 :#line:797
                    return #line:798
                OOOOO0OOO000O00O0 =_OO00OO00OOOO0O0OO [-1 ]-1 #line:799
            _O0O0OOOOO0000000O .append (OOOOO0OOO000O00O0 )#line:801
        elif _O00OO000000O00OO0 =="one":#line:802
            if len (_OO00OO00OOOO0O0OO )==0 :#line:803
                OO0OO0O00OOO000O0 =OOOO0O00O0000O0OO .data ["varname"].index (OOOOO00OO0O0O0000 ['defi'].get ('attributes')[_O00000OO0000O00OO [-1 ]].get ('name'))#line:804
                try :#line:805
                    OOOOO0OOO000O00O0 =OOOO0O00O0000O0OO .data ["catnames"][OO0OO0O00OOO000O0 ].index (OOOOO00OO0O0O0000 ['defi'].get ('attributes')[_O00000OO0000O00OO [-1 ]].get ('value'))#line:806
                except :#line:807
                    print (f"ERROR: attribute '{OOOOO00OO0O0O0000['defi'].get('attributes')[_O00000OO0000O00OO[-1]].get('name')}' has not value '{OOOOO00OO0O0O0000['defi'].get('attributes')[_O00000OO0000O00OO[-1]].get('value')}'")#line:808
                    exit (1 )#line:809
                _O0O0OOOOO0000000O .append (OOOOO0OOO000O00O0 )#line:810
                _O0OO00OO0O0OOO000 =1 #line:811
                _OO000O000OO0OO0OO =1 #line:812
            else :#line:813
                print ("DEBUG: one category should not have more categories")#line:814
                return #line:815
        else :#line:816
            print ("Attribute type "+_O00OO000000O00OO0 +" not supported.")#line:817
            return #line:818
        for O0O00OO0O0O0OOO00 in _O0O0OOOOO0000000O :#line:821
                _OO00OO00OOOO0O0OO .append (O0O00OO0O0O0OOO00 )#line:823
                _O000000O000O000O0 .pop ()#line:824
                _O000000O000O000O0 .append (_OO00OO00OOOO0O0OO )#line:825
                _OO0OO0O00OO0O0000 =_O00OO0OOOOOO0000O |OOOO0O00O0000O0OO .data ["dm"][OOOO0O00O0000O0OO .data ["varname"].index (OOOOO00OO0O0O0000 ['defi'].get ('attributes')[_O00000OO0000O00OO [-1 ]].get ('name'))][O0O00OO0O0O0OOO00 ]#line:829
                _O00OOOO0OO00O0OOO =1 #line:831
                if (len (_O00000OO0000O00OO )<_OO000O0OO0O0OO00O ):#line:832
                    _O00OOOO0OO00O0OOO =-1 #line:833
                if (len (_O000000O000O000O0 [-1 ])<_O0OO00OO0O0OOO000 ):#line:835
                    _O00OOOO0OO00O0OOO =0 #line:836
                _OO0OO00O0O00OOO0O =0 #line:838
                if OOOOO00OO0O0O0000 ['defi'].get ('type')=='con':#line:839
                    _OO0OO00O0O00OOO0O =_OOOO0OOOO00O00O00 &_OO0OO0O00OO0O0000 #line:840
                else :#line:841
                    _OO0OO00O0O00OOO0O =_OOOO0OOOO00O00O00 |_OO0OO0O00OO0O0000 #line:842
                OOOOO00OO0O0O0000 ['trace_cedent']=_O00000OO0000O00OO #line:843
                OOOOO00OO0O0O0000 ['traces']=_O000000O000O000O0 #line:844
                OOOOO00OO0O0O0000 ['generated_string']=OOOO0O00O0000O0OO ._print (OOOOO00OO0O0O0000 ,_O00000OO0000O00OO ,_O000000O000O000O0 )#line:845
                OOOOO00OO0O0O0000 ['filter_value']=_OO0OO00O0O00OOO0O #line:846
                OO0O00O0OO0000000 ['cedents'].append (OOOOO00OO0O0O0000 )#line:847
                OOO0000O0OO000O00 =OOOO0O00O0000O0OO ._verify_opt (OO0O00O0OO0000000 ,OOOOO00OO0O0O0000 )#line:848
                if not (OOO0000O0OO000O00 ):#line:854
                    if _O00OOOO0OO00O0OOO ==1 :#line:855
                        if len (OO0O00O0OO0000000 ['cedents_to_do'])==len (OO0O00O0OO0000000 ['cedents']):#line:857
                            if OOOO0O00O0000O0OO .proc =='CFMiner':#line:858
                                OOO0O0O0OOO0OO000 ,O0OO0O00OOO0OO0O0 =OOOO0O00O0000O0OO ._verifyCF (_OO0OO00O0O00OOO0O )#line:859
                            elif OOOO0O00O0000O0OO .proc =='4ftMiner':#line:860
                                OOO0O0O0OOO0OO000 ,O0OO0O00OOO0OO0O0 =OOOO0O00O0000O0OO ._verify4ft (_OO0OO0O00OO0O0000 )#line:861
                            elif OOOO0O00O0000O0OO .proc =='SD4ftMiner':#line:862
                                OOO0O0O0OOO0OO000 ,O0OO0O00OOO0OO0O0 =OOOO0O00O0000O0OO ._verifysd4ft (_OO0OO0O00OO0O0000 )#line:863
                            elif OOOO0O00O0000O0OO .proc =='NewAct4ftMiner':#line:864
                                OOO0O0O0OOO0OO000 ,O0OO0O00OOO0OO0O0 =OOOO0O00O0000O0OO ._verifynewact4ft (_OO0OO0O00OO0O0000 )#line:865
                            elif OOOO0O00O0000O0OO .proc =='Act4ftMiner':#line:866
                                OOO0O0O0OOO0OO000 ,O0OO0O00OOO0OO0O0 =OOOO0O00O0000O0OO ._verifyact4ft (_OO0OO0O00OO0O0000 )#line:867
                            else :#line:868
                                print ("Unsupported procedure : "+OOOO0O00O0000O0OO .proc )#line:869
                                exit (0 )#line:870
                            if OOO0O0O0OOO0OO000 ==True :#line:871
                                OO00O0OO0OO00O00O ={}#line:872
                                OO00O0OO0OO00O00O ["rule_id"]=OOOO0O00O0000O0OO .stats ['total_valid']#line:873
                                OO00O0OO0OO00O00O ["cedents"]={}#line:874
                                for O0O0O00O0OO0O00OO in OO0O00O0OO0000000 ['cedents']:#line:875
                                    OO00O0OO0OO00O00O ['cedents'][O0O0O00O0OO0O00OO ['cedent_type']]=O0O0O00O0OO0O00OO ['generated_string']#line:876
                                OO00O0OO0OO00O00O ["params"]=O0OO0O00OOO0OO0O0 #line:878
                                OO00O0OO0OO00O00O ["trace_cedent"]=_O00000OO0000O00OO #line:879
                                OOOO0O00O0000O0OO ._print_rule (OO00O0OO0OO00O00O )#line:880
                                OO00O0OO0OO00O00O ["traces"]=_O000000O000O000O0 #line:883
                                OOOO0O00O0000O0OO .rulelist .append (OO00O0OO0OO00O00O )#line:884
                            OOOO0O00O0000O0OO .stats ['total_cnt']+=1 #line:885
                    if _O00OOOO0OO00O0OOO >=0 :#line:886
                        if len (OO0O00O0OO0000000 ['cedents_to_do'])>len (OO0O00O0OO0000000 ['cedents']):#line:887
                            OOOO0O00O0000O0OO ._start_cedent (OO0O00O0OO0000000 )#line:888
                    OO0O00O0OO0000000 ['cedents'].pop ()#line:889
                    if (len (_O00000OO0000O00OO )<_OOOO0O00O00O0O000 ):#line:890
                        OOOO0O00O0000O0OO ._genvar (OO0O00O0OO0000000 ,OOOOO00OO0O0O0000 ,_O00000OO0000O00OO ,_O000000O000O000O0 ,_OO0OO00O0O00OOO0O ,_OO000O0OO0O0OO00O ,_OOOO0O00O00O0O000 )#line:891
                else :#line:892
                    OO0O00O0OO0000000 ['cedents'].pop ()#line:893
                if len (_OO00OO00OOOO0O0OO )<_OO000O000OO0OO0OO :#line:894
                    OOOO0O00O0000O0OO ._gencomb (OO0O00O0OO0000000 ,OOOOO00OO0O0O0000 ,_O00000OO0000O00OO ,_O000000O000O000O0 ,_OO00OO00OOOO0O0OO ,_OOOO0OOOO00O00O00 ,_OO0OO0O00OO0O0000 ,O00000O00OOO0OOOO ,_O00OO000000O00OO0 ,_OO000O0OO0O0OO00O ,_OOOO0O00O00O0O000 ,_O0OO00OO0O0OOO000 ,_OO000O000OO0OO0OO )#line:895
                _OO00OO00OOOO0O0OO .pop ()#line:896
    def _start_cedent (O0000OOO0O0O00OO0 ,O0OOO00O0OO0OOOOO ):#line:898
        if len (O0OOO00O0OO0OOOOO ['cedents_to_do'])>len (O0OOO00O0OO0OOOOO ['cedents']):#line:899
            _O0000OOOOOO0OOOO0 =[]#line:900
            _O0O0OOOOO00OOO0O0 =[]#line:901
            OO0OO0O00O00OOOO0 ={}#line:902
            OO0OO0O00O00OOOO0 ['cedent_type']=O0OOO00O0OO0OOOOO ['cedents_to_do'][len (O0OOO00O0OO0OOOOO ['cedents'])]#line:903
            O0000O00OO0O0OO0O =OO0OO0O00O00OOOO0 ['cedent_type']#line:904
            if ((O0000O00OO0O0OO0O [-1 ]=='-')|(O0000O00OO0O0OO0O [-1 ]=='+')):#line:905
                O0000O00OO0O0OO0O =O0000O00OO0O0OO0O [:-1 ]#line:906
            OO0OO0O00O00OOOO0 ['defi']=O0000OOO0O0O00OO0 .kwargs .get (O0000O00OO0O0OO0O )#line:908
            if (OO0OO0O00O00OOOO0 ['defi']==None ):#line:909
                print ("Error getting cedent ",OO0OO0O00O00OOOO0 ['cedent_type'])#line:910
            _O0OO0O0O00O0O0000 =int (0 )#line:911
            OO0OO0O00O00OOOO0 ['num_cedent']=len (OO0OO0O00O00OOOO0 ['defi'].get ('attributes'))#line:916
            if (OO0OO0O00O00OOOO0 ['defi'].get ('type')=='con'):#line:917
                _O0OO0O0O00O0O0000 =(1 <<O0000OOO0O0O00OO0 .data ["rows_count"])-1 #line:918
            O0000OOO0O0O00OO0 ._genvar (O0OOO00O0OO0OOOOO ,OO0OO0O00O00OOOO0 ,_O0000OOOOOO0OOOO0 ,_O0O0OOOOO00OOO0O0 ,_O0OO0O0O00O0O0000 ,OO0OO0O00O00OOOO0 ['defi'].get ('minlen'),OO0OO0O00O00OOOO0 ['defi'].get ('maxlen'))#line:919
    def _calc_all (OOO00O00000000000 ,**OOO0OOOOO0O000000 ):#line:922
        OOO00O00000000000 ._prep_data (OOO00O00000000000 .kwargs .get ("df"))#line:923
        OOO00O00000000000 ._calculate (**OOO0OOOOO0O000000 )#line:924
    def _check_cedents (OO0O000O00O0OOO00 ,OOOOO000OOO00OO00 ,**O0OO0OOOOOOOOO00O ):#line:926
        O000OOO0OO00O0OOO =True #line:927
        if (O0OO0OOOOOOOOO00O .get ('quantifiers',None )==None ):#line:928
            print (f"Error: missing quantifiers.")#line:929
            O000OOO0OO00O0OOO =False #line:930
            return O000OOO0OO00O0OOO #line:931
        if (type (O0OO0OOOOOOOOO00O .get ('quantifiers'))!=dict ):#line:932
            print (f"Error: quantifiers are not dictionary type.")#line:933
            O000OOO0OO00O0OOO =False #line:934
            return O000OOO0OO00O0OOO #line:935
        for OO000O000OO000OOO in OOOOO000OOO00OO00 :#line:937
            if (O0OO0OOOOOOOOO00O .get (OO000O000OO000OOO ,None )==None ):#line:938
                print (f"Error: cedent {OO000O000OO000OOO} is missing in parameters.")#line:939
                O000OOO0OO00O0OOO =False #line:940
                return O000OOO0OO00O0OOO #line:941
            OOOOOO0OO0OOOO00O =O0OO0OOOOOOOOO00O .get (OO000O000OO000OOO )#line:942
            if (OOOOOO0OO0OOOO00O .get ('minlen'),None )==None :#line:943
                print (f"Error: cedent {OO000O000OO000OOO} has no minimal length specified.")#line:944
                O000OOO0OO00O0OOO =False #line:945
                return O000OOO0OO00O0OOO #line:946
            if not (type (OOOOOO0OO0OOOO00O .get ('minlen'))is int ):#line:947
                print (f"Error: cedent {OO000O000OO000OOO} has invalid type of minimal length ({type(OOOOOO0OO0OOOO00O.get('minlen'))}).")#line:948
                O000OOO0OO00O0OOO =False #line:949
                return O000OOO0OO00O0OOO #line:950
            if (OOOOOO0OO0OOOO00O .get ('maxlen'),None )==None :#line:951
                print (f"Error: cedent {OO000O000OO000OOO} has no maximal length specified.")#line:952
                O000OOO0OO00O0OOO =False #line:953
                return O000OOO0OO00O0OOO #line:954
            if not (type (OOOOOO0OO0OOOO00O .get ('maxlen'))is int ):#line:955
                print (f"Error: cedent {OO000O000OO000OOO} has invalid type of maximal length.")#line:956
                O000OOO0OO00O0OOO =False #line:957
                return O000OOO0OO00O0OOO #line:958
            if (OOOOOO0OO0OOOO00O .get ('type'),None )==None :#line:959
                print (f"Error: cedent {OO000O000OO000OOO} has no type specified.")#line:960
                O000OOO0OO00O0OOO =False #line:961
                return O000OOO0OO00O0OOO #line:962
            if not ((OOOOOO0OO0OOOO00O .get ('type'))in (['con','dis'])):#line:963
                print (f"Error: cedent {OO000O000OO000OOO} has invalid type. Allowed values are 'con' and 'dis'.")#line:964
                O000OOO0OO00O0OOO =False #line:965
                return O000OOO0OO00O0OOO #line:966
            if (OOOOOO0OO0OOOO00O .get ('attributes'),None )==None :#line:967
                print (f"Error: cedent {OO000O000OO000OOO} has no attributes specified.")#line:968
                O000OOO0OO00O0OOO =False #line:969
                return O000OOO0OO00O0OOO #line:970
            for O00O0OO0O00OOOOO0 in OOOOOO0OO0OOOO00O .get ('attributes'):#line:971
                if (O00O0OO0O00OOOOO0 .get ('name'),None )==None :#line:972
                    print (f"Error: cedent {OO000O000OO000OOO} / attribute {O00O0OO0O00OOOOO0} has no 'name' attribute specified.")#line:973
                    O000OOO0OO00O0OOO =False #line:974
                    return O000OOO0OO00O0OOO #line:975
                if not ((O00O0OO0O00OOOOO0 .get ('name'))in OO0O000O00O0OOO00 .data ["varname"]):#line:976
                    print (f"Error: cedent {OO000O000OO000OOO} / attribute {O00O0OO0O00OOOOO0.get('name')} not in variable list. Please check spelling.")#line:977
                    O000OOO0OO00O0OOO =False #line:978
                    return O000OOO0OO00O0OOO #line:979
                if (O00O0OO0O00OOOOO0 .get ('type'),None )==None :#line:980
                    print (f"Error: cedent {OO000O000OO000OOO} / attribute {O00O0OO0O00OOOOO0.get('name')} has no 'type' attribute specified.")#line:981
                    O000OOO0OO00O0OOO =False #line:982
                    return O000OOO0OO00O0OOO #line:983
                if not ((O00O0OO0O00OOOOO0 .get ('type'))in (['rcut','lcut','seq','subset','one'])):#line:984
                    print (f"Error: cedent {OO000O000OO000OOO} / attribute {O00O0OO0O00OOOOO0.get('name')} has unsupported type {O00O0OO0O00OOOOO0.get('type')}. Supported types are 'subset','seq','lcut','rcut','one'.")#line:985
                    O000OOO0OO00O0OOO =False #line:986
                    return O000OOO0OO00O0OOO #line:987
                if (O00O0OO0O00OOOOO0 .get ('minlen'),None )==None :#line:988
                    print (f"Error: cedent {OO000O000OO000OOO} / attribute {O00O0OO0O00OOOOO0.get('name')} has no minimal length specified.")#line:989
                    O000OOO0OO00O0OOO =False #line:990
                    return O000OOO0OO00O0OOO #line:991
                if not (type (O00O0OO0O00OOOOO0 .get ('minlen'))is int ):#line:992
                    if not (O00O0OO0O00OOOOO0 .get ('type')=='one'):#line:993
                        print (f"Error: cedent {OO000O000OO000OOO} / attribute {O00O0OO0O00OOOOO0.get('name')} has invalid type of minimal length.")#line:994
                        O000OOO0OO00O0OOO =False #line:995
                        return O000OOO0OO00O0OOO #line:996
                if (O00O0OO0O00OOOOO0 .get ('maxlen'),None )==None :#line:997
                    print (f"Error: cedent {OO000O000OO000OOO} / attribute {O00O0OO0O00OOOOO0.get('name')} has no maximal length specified.")#line:998
                    O000OOO0OO00O0OOO =False #line:999
                    return O000OOO0OO00O0OOO #line:1000
                if not (type (O00O0OO0O00OOOOO0 .get ('maxlen'))is int ):#line:1001
                    if not (O00O0OO0O00OOOOO0 .get ('type')=='one'):#line:1002
                        print (f"Error: cedent {OO000O000OO000OOO} / attribute {O00O0OO0O00OOOOO0.get('name')} has invalid type of maximal length.")#line:1003
                        O000OOO0OO00O0OOO =False #line:1004
                        return O000OOO0OO00O0OOO #line:1005
        return O000OOO0OO00O0OOO #line:1006
    def _calculate (O00OO00000O000O00 ,**O0O0OO00O00O0OO00 ):#line:1008
        if O00OO00000O000O00 .data ["data_prepared"]==0 :#line:1009
            print ("Error: data not prepared")#line:1010
            return #line:1011
        O00OO00000O000O00 .kwargs =O0O0OO00O00O0OO00 #line:1012
        O00OO00000O000O00 .proc =O0O0OO00O00O0OO00 .get ('proc')#line:1013
        O00OO00000O000O00 .quantifiers =O0O0OO00O00O0OO00 .get ('quantifiers')#line:1014
        O00OO00000O000O00 ._init_task ()#line:1016
        O00OO00000O000O00 .stats ['start_proc_time']=time .time ()#line:1017
        O00OO00000O000O00 .task_actinfo ['cedents_to_do']=[]#line:1018
        O00OO00000O000O00 .task_actinfo ['cedents']=[]#line:1019
        if O0O0OO00O00O0OO00 .get ("proc")=='CFMiner':#line:1022
            O00OO00000O000O00 .task_actinfo ['cedents_to_do']=['cond']#line:1023
            if O0O0OO00O00O0OO00 .get ('target',None )==None :#line:1024
                print ("ERROR: no target variable defined for CF Miner")#line:1025
                return #line:1026
            if not (O00OO00000O000O00 ._check_cedents (['cond'],**O0O0OO00O00O0OO00 )):#line:1027
                return #line:1028
            if not (O0O0OO00O00O0OO00 .get ('target')in O00OO00000O000O00 .data ["varname"]):#line:1029
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:1030
                return #line:1031
        elif O0O0OO00O00O0OO00 .get ("proc")=='4ftMiner':#line:1033
            if not (O00OO00000O000O00 ._check_cedents (['ante','succ'],**O0O0OO00O00O0OO00 )):#line:1034
                return #line:1035
            _O0OO0OOOOO0OOO0O0 =O0O0OO00O00O0OO00 .get ("cond")#line:1037
            if _O0OO0OOOOO0OOO0O0 !=None :#line:1038
                O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('cond')#line:1039
            else :#line:1040
                OO0OO0OO0O0O00OOO =O00OO00000O000O00 .cedent #line:1041
                OO0OO0OO0O0O00OOO ['cedent_type']='cond'#line:1042
                OO0OO0OO0O0O00OOO ['filter_value']=(1 <<O00OO00000O000O00 .data ["rows_count"])-1 #line:1043
                OO0OO0OO0O0O00OOO ['generated_string']='---'#line:1044
                O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('cond')#line:1046
                O00OO00000O000O00 .task_actinfo ['cedents'].append (OO0OO0OO0O0O00OOO )#line:1047
            O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('ante')#line:1051
            O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('succ')#line:1052
        elif O0O0OO00O00O0OO00 .get ("proc")=='NewAct4ftMiner':#line:1053
            _O0OO0OOOOO0OOO0O0 =O0O0OO00O00O0OO00 .get ("cond")#line:1056
            if _O0OO0OOOOO0OOO0O0 !=None :#line:1057
                O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('cond')#line:1058
            else :#line:1059
                OO0OO0OO0O0O00OOO =O00OO00000O000O00 .cedent #line:1060
                OO0OO0OO0O0O00OOO ['cedent_type']='cond'#line:1061
                OO0OO0OO0O0O00OOO ['filter_value']=(1 <<O00OO00000O000O00 .data ["rows_count"])-1 #line:1062
                OO0OO0OO0O0O00OOO ['generated_string']='---'#line:1063
                print (OO0OO0OO0O0O00OOO ['filter_value'])#line:1064
                O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('cond')#line:1065
                O00OO00000O000O00 .task_actinfo ['cedents'].append (OO0OO0OO0O0O00OOO )#line:1066
            O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('antv')#line:1067
            O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('sucv')#line:1068
            O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('ante')#line:1069
            O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('succ')#line:1070
        elif O0O0OO00O00O0OO00 .get ("proc")=='Act4ftMiner':#line:1071
            _O0OO0OOOOO0OOO0O0 =O0O0OO00O00O0OO00 .get ("cond")#line:1074
            if _O0OO0OOOOO0OOO0O0 !=None :#line:1075
                O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('cond')#line:1076
            else :#line:1077
                OO0OO0OO0O0O00OOO =O00OO00000O000O00 .cedent #line:1078
                OO0OO0OO0O0O00OOO ['cedent_type']='cond'#line:1079
                OO0OO0OO0O0O00OOO ['filter_value']=(1 <<O00OO00000O000O00 .data ["rows_count"])-1 #line:1080
                OO0OO0OO0O0O00OOO ['generated_string']='---'#line:1081
                print (OO0OO0OO0O0O00OOO ['filter_value'])#line:1082
                O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('cond')#line:1083
                O00OO00000O000O00 .task_actinfo ['cedents'].append (OO0OO0OO0O0O00OOO )#line:1084
            O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('antv-')#line:1085
            O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('antv+')#line:1086
            O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('sucv-')#line:1087
            O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('sucv+')#line:1088
            O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('ante')#line:1089
            O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('succ')#line:1090
        elif O0O0OO00O00O0OO00 .get ("proc")=='SD4ftMiner':#line:1091
            if not (O00OO00000O000O00 ._check_cedents (['ante','succ','frst','scnd'],**O0O0OO00O00O0OO00 )):#line:1094
                return #line:1095
            _O0OO0OOOOO0OOO0O0 =O0O0OO00O00O0OO00 .get ("cond")#line:1096
            if _O0OO0OOOOO0OOO0O0 !=None :#line:1097
                O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('cond')#line:1098
            else :#line:1099
                OO0OO0OO0O0O00OOO =O00OO00000O000O00 .cedent #line:1100
                OO0OO0OO0O0O00OOO ['cedent_type']='cond'#line:1101
                OO0OO0OO0O0O00OOO ['filter_value']=(1 <<O00OO00000O000O00 .data ["rows_count"])-1 #line:1102
                OO0OO0OO0O0O00OOO ['generated_string']='---'#line:1103
                O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('cond')#line:1105
                O00OO00000O000O00 .task_actinfo ['cedents'].append (OO0OO0OO0O0O00OOO )#line:1106
            O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('frst')#line:1107
            O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('scnd')#line:1108
            O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('ante')#line:1109
            O00OO00000O000O00 .task_actinfo ['cedents_to_do'].append ('succ')#line:1110
        else :#line:1111
            print ("Unsupported procedure")#line:1112
            return #line:1113
        print ("Will go for ",O0O0OO00O00O0OO00 .get ("proc"))#line:1114
        O00OO00000O000O00 .task_actinfo ['optim']={}#line:1117
        O000O0O00O0O00OOO =True #line:1118
        for O0OO0OOO00000O000 in O00OO00000O000O00 .task_actinfo ['cedents_to_do']:#line:1119
            try :#line:1120
                OOOOO0OOOOO0OOO0O =O00OO00000O000O00 .kwargs .get (O0OO0OOO00000O000 )#line:1121
                if OOOOO0OOOOO0OOO0O .get ('type')!='con':#line:1124
                    O000O0O00O0O00OOO =False #line:1125
            except :#line:1126
                OO000O0OO000OO0O0 =1 <2 #line:1127
        if "opts"in O0O0OO00O00O0OO00 :#line:1129
            if "no_optimizations"in O0O0OO00O00O0OO00 .get ('opts'):#line:1130
                O000O0O00O0O00OOO =False #line:1131
                print ("No optimization will be made.")#line:1132
        O000O00OOOO0OOOOO ={}#line:1134
        O000O00OOOO0OOOOO ['only_con']=O000O0O00O0O00OOO #line:1135
        O00OO00000O000O00 .task_actinfo ['optim']=O000O00OOOO0OOOOO #line:1136
        print ("Starting to mine rules.")#line:1144
        O00OO00000O000O00 ._start_cedent (O00OO00000O000O00 .task_actinfo )#line:1145
        O00OO00000O000O00 .stats ['end_proc_time']=time .time ()#line:1147
        print ("Done. Total verifications : "+str (O00OO00000O000O00 .stats ['total_cnt'])+", rules "+str (O00OO00000O000O00 .stats ['total_valid'])+",control number:"+str (O00OO00000O000O00 .stats ['control_number'])+", times: prep "+str (O00OO00000O000O00 .stats ['end_prep_time']-O00OO00000O000O00 .stats ['start_prep_time'])+", processing "+str (O00OO00000O000O00 .stats ['end_proc_time']-O00OO00000O000O00 .stats ['start_proc_time']))#line:1150
        O0000OOOO000O0OOO ={}#line:1151
        O0OOO0O0OO0OOOOOO ={}#line:1152
        O0OOO0O0OO0OOOOOO ["task_type"]=O0O0OO00O00O0OO00 .get ('proc')#line:1153
        O0OOO0O0OO0OOOOOO ["target"]=O0O0OO00O00O0OO00 .get ('target')#line:1155
        O0OOO0O0OO0OOOOOO ["self.quantifiers"]=O00OO00000O000O00 .quantifiers #line:1156
        if O0O0OO00O00O0OO00 .get ('cond')!=None :#line:1158
            O0OOO0O0OO0OOOOOO ['cond']=O0O0OO00O00O0OO00 .get ('cond')#line:1159
        if O0O0OO00O00O0OO00 .get ('ante')!=None :#line:1160
            O0OOO0O0OO0OOOOOO ['ante']=O0O0OO00O00O0OO00 .get ('ante')#line:1161
        if O0O0OO00O00O0OO00 .get ('succ')!=None :#line:1162
            O0OOO0O0OO0OOOOOO ['succ']=O0O0OO00O00O0OO00 .get ('succ')#line:1163
        if O0O0OO00O00O0OO00 .get ('opts')!=None :#line:1164
            O0OOO0O0OO0OOOOOO ['opts']=O0O0OO00O00O0OO00 .get ('opts')#line:1165
        O0000OOOO000O0OOO ["taskinfo"]=O0OOO0O0OO0OOOOOO #line:1166
        O0OO00OO000O000OO ={}#line:1167
        O0OO00OO000O000OO ["total_verifications"]=O00OO00000O000O00 .stats ['total_cnt']#line:1168
        O0OO00OO000O000OO ["valid_rules"]=O00OO00000O000O00 .stats ['total_valid']#line:1169
        O0OO00OO000O000OO ["time_prep"]=O00OO00000O000O00 .stats ['end_prep_time']-O00OO00000O000O00 .stats ['start_prep_time']#line:1170
        O0OO00OO000O000OO ["time_processing"]=O00OO00000O000O00 .stats ['end_proc_time']-O00OO00000O000O00 .stats ['start_proc_time']#line:1171
        O0OO00OO000O000OO ["time_total"]=O00OO00000O000O00 .stats ['end_prep_time']-O00OO00000O000O00 .stats ['start_prep_time']+O00OO00000O000O00 .stats ['end_proc_time']-O00OO00000O000O00 .stats ['start_proc_time']#line:1172
        O0000OOOO000O0OOO ["summary_statistics"]=O0OO00OO000O000OO #line:1173
        O0000OOOO000O0OOO ["rules"]=O00OO00000O000O00 .rulelist #line:1174
        OOO00O0000O0O0O00 ={}#line:1175
        OOO00O0000O0O0O00 ["varname"]=O00OO00000O000O00 .data ["varname"]#line:1176
        OOO00O0000O0O0O00 ["catnames"]=O00OO00000O000O00 .data ["catnames"]#line:1177
        O0000OOOO000O0OOO ["datalabels"]=OOO00O0000O0O0O00 #line:1178
        O00OO00000O000O00 .result =O0000OOOO000O0OOO #line:1181
    def print_summary (O0O0O00000OOOO0O0 ):#line:1183
        print ("")#line:1184
        print ("CleverMiner task processing summary:")#line:1185
        print ("")#line:1186
        print (f"Task type : {O0O0O00000OOOO0O0.result['taskinfo']['task_type']}")#line:1187
        print (f"Number of verifications : {O0O0O00000OOOO0O0.result['summary_statistics']['total_verifications']}")#line:1188
        print (f"Number of rules : {O0O0O00000OOOO0O0.result['summary_statistics']['valid_rules']}")#line:1189
        print (f"Total time needed : {strftime('%Hh %Mm %Ss', gmtime(O0O0O00000OOOO0O0.result['summary_statistics']['time_total']))}")#line:1190
        print (f"Time of data preparation : {strftime('%Hh %Mm %Ss', gmtime(O0O0O00000OOOO0O0.result['summary_statistics']['time_prep']))}")#line:1192
        print (f"Time of rule mining : {strftime('%Hh %Mm %Ss', gmtime(O0O0O00000OOOO0O0.result['summary_statistics']['time_processing']))}")#line:1193
        print ("")#line:1194
    def print_hypolist (OO00000O0O000OO0O ):#line:1196
        OO00000O0O000OO0O .print_rulelist ();#line:1197
    def print_rulelist (O0O0O000OO000O000 ):#line:1199
        print ("")#line:1201
        print ("List of rules:")#line:1202
        if O0O0O000OO000O000 .result ['taskinfo']['task_type']=="4ftMiner":#line:1203
            print ("RULEID BASE  CONF  AAD    Rule")#line:1204
        elif O0O0O000OO000O000 .result ['taskinfo']['task_type']=="CFMiner":#line:1205
            print ("RULEID BASE  S_UP  S_DOWN Condition")#line:1206
        elif O0O0O000OO000O000 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1207
            print ("RULEID BASE1 BASE2 RatioConf DeltaConf Rule")#line:1208
        else :#line:1209
            print ("Unsupported task type for rulelist")#line:1210
            return #line:1211
        for OOOO0OO0OOOOO0O00 in O0O0O000OO000O000 .result ["rules"]:#line:1212
            OOO0OOO0O0O0000O0 ="{:6d}".format (OOOO0OO0OOOOO0O00 ["rule_id"])#line:1213
            if O0O0O000OO000O000 .result ['taskinfo']['task_type']=="4ftMiner":#line:1214
                OOO0OOO0O0O0000O0 =OOO0OOO0O0O0000O0 +" "+"{:5d}".format (OOOO0OO0OOOOO0O00 ["params"]["base"])+" "+"{:.3f}".format (OOOO0OO0OOOOO0O00 ["params"]["conf"])+" "+"{:+.3f}".format (OOOO0OO0OOOOO0O00 ["params"]["aad"])#line:1215
                OOO0OOO0O0O0000O0 =OOO0OOO0O0O0000O0 +" "+OOOO0OO0OOOOO0O00 ["cedents"]["ante"]+" => "+OOOO0OO0OOOOO0O00 ["cedents"]["succ"]+" | "+OOOO0OO0OOOOO0O00 ["cedents"]["cond"]#line:1216
            elif O0O0O000OO000O000 .result ['taskinfo']['task_type']=="CFMiner":#line:1217
                OOO0OOO0O0O0000O0 =OOO0OOO0O0O0000O0 +" "+"{:5d}".format (OOOO0OO0OOOOO0O00 ["params"]["base"])+" "+"{:5d}".format (OOOO0OO0OOOOO0O00 ["params"]["s_up"])+" "+"{:5d}".format (OOOO0OO0OOOOO0O00 ["params"]["s_down"])#line:1218
                OOO0OOO0O0O0000O0 =OOO0OOO0O0O0000O0 +" "+OOOO0OO0OOOOO0O00 ["cedents"]["cond"]#line:1219
            elif O0O0O000OO000O000 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1220
                OOO0OOO0O0O0000O0 =OOO0OOO0O0O0000O0 +" "+"{:5d}".format (OOOO0OO0OOOOO0O00 ["params"]["base1"])+" "+"{:5d}".format (OOOO0OO0OOOOO0O00 ["params"]["base2"])+"    "+"{:.3f}".format (OOOO0OO0OOOOO0O00 ["params"]["ratioconf"])+"    "+"{:+.3f}".format (OOOO0OO0OOOOO0O00 ["params"]["deltaconf"])#line:1221
                OOO0OOO0O0O0000O0 =OOO0OOO0O0O0000O0 +"  "+OOOO0OO0OOOOO0O00 ["cedents"]["ante"]+" => "+OOOO0OO0OOOOO0O00 ["cedents"]["succ"]+" | "+OOOO0OO0OOOOO0O00 ["cedents"]["cond"]+" : "+OOOO0OO0OOOOO0O00 ["cedents"]["frst"]+" x "+OOOO0OO0OOOOO0O00 ["cedents"]["scnd"]#line:1222
            print (OOO0OOO0O0O0000O0 )#line:1224
        print ("")#line:1225
    def print_hypo (OOO0000OOOO0000O0 ,OO0OOOOO0O00OOOO0 ):#line:1227
        OOO0000OOOO0000O0 .print_rule (OO0OOOOO0O00OOOO0 )#line:1228
    def print_rule (O0000O00000OO00O0 ,OOO00000O0OOO00OO ):#line:1231
        print ("")#line:1232
        if (OOO00000O0OOO00OO <=len (O0000O00000OO00O0 .result ["rules"])):#line:1233
            if O0000O00000OO00O0 .result ['taskinfo']['task_type']=="4ftMiner":#line:1234
                print ("")#line:1235
                O0OO0O0OOO0OO0OOO =O0000O00000OO00O0 .result ["rules"][OOO00000O0OOO00OO -1 ]#line:1236
                print (f"Rule id : {O0OO0O0OOO0OO0OOO['rule_id']}")#line:1237
                print ("")#line:1238
                print (f"Base : {'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['base'])}  Relative base : {'{:.3f}'.format(O0OO0O0OOO0OO0OOO['params']['rel_base'])}  CONF : {'{:.3f}'.format(O0OO0O0OOO0OO0OOO['params']['conf'])}  AAD : {'{:+.3f}'.format(O0OO0O0OOO0OO0OOO['params']['aad'])}  BAD : {'{:+.3f}'.format(O0OO0O0OOO0OO0OOO['params']['bad'])}")#line:1239
                print ("")#line:1240
                print ("Cedents:")#line:1241
                print (f"  antecedent : {O0OO0O0OOO0OO0OOO['cedents']['ante']}")#line:1242
                print (f"  succcedent : {O0OO0O0OOO0OO0OOO['cedents']['succ']}")#line:1243
                print (f"  condition  : {O0OO0O0OOO0OO0OOO['cedents']['cond']}")#line:1244
                print ("")#line:1245
                print ("Fourfold table")#line:1246
                print (f"    |  S  |  ¬S |")#line:1247
                print (f"----|-----|-----|")#line:1248
                print (f" A  |{'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['fourfold'][0])}|{'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['fourfold'][1])}|")#line:1249
                print (f"----|-----|-----|")#line:1250
                print (f"¬A  |{'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['fourfold'][2])}|{'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['fourfold'][3])}|")#line:1251
                print (f"----|-----|-----|")#line:1252
            elif O0000O00000OO00O0 .result ['taskinfo']['task_type']=="CFMiner":#line:1253
                print ("")#line:1254
                O0OO0O0OOO0OO0OOO =O0000O00000OO00O0 .result ["rules"][OOO00000O0OOO00OO -1 ]#line:1255
                print (f"Rule id : {O0OO0O0OOO0OO0OOO['rule_id']}")#line:1256
                print ("")#line:1257
                print (f"Base : {'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['base'])}  Relative base : {'{:.3f}'.format(O0OO0O0OOO0OO0OOO['params']['rel_base'])}  Steps UP (consecutive) : {'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['s_up'])}  Steps DOWN (consecutive) : {'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['s_down'])}  Steps UP (any) : {'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['s_any_up'])}  Steps DOWN (any) : {'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['s_any_down'])}  Histogram maximum : {'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['max'])}  Histogram minimum : {'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['min'])}  Histogram relative maximum : {'{:.3f}'.format(O0OO0O0OOO0OO0OOO['params']['rel_max'])} Histogram relative minimum : {'{:.3f}'.format(O0OO0O0OOO0OO0OOO['params']['rel_min'])}")#line:1259
                print ("")#line:1260
                print (f"Condition  : {O0OO0O0OOO0OO0OOO['cedents']['cond']}")#line:1261
                print ("")#line:1262
                print (f"Histogram {O0OO0O0OOO0OO0OOO['params']['hist']}")#line:1263
            elif O0000O00000OO00O0 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1264
                print ("")#line:1265
                O0OO0O0OOO0OO0OOO =O0000O00000OO00O0 .result ["rules"][OOO00000O0OOO00OO -1 ]#line:1266
                print (f"Rule id : {O0OO0O0OOO0OO0OOO['rule_id']}")#line:1267
                print ("")#line:1268
                print (f"Base1 : {'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['base1'])} Base2 : {'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['base2'])}  Relative base 1 : {'{:.3f}'.format(O0OO0O0OOO0OO0OOO['params']['rel_base1'])} Relative base 2 : {'{:.3f}'.format(O0OO0O0OOO0OO0OOO['params']['rel_base2'])} CONF1 : {'{:.3f}'.format(O0OO0O0OOO0OO0OOO['params']['conf1'])}  CONF2 : {'{:+.3f}'.format(O0OO0O0OOO0OO0OOO['params']['conf2'])}  Delta Conf : {'{:+.3f}'.format(O0OO0O0OOO0OO0OOO['params']['deltaconf'])} Ratio Conf : {'{:+.3f}'.format(O0OO0O0OOO0OO0OOO['params']['ratioconf'])}")#line:1269
                print ("")#line:1270
                print ("Cedents:")#line:1271
                print (f"  antecedent : {O0OO0O0OOO0OO0OOO['cedents']['ante']}")#line:1272
                print (f"  succcedent : {O0OO0O0OOO0OO0OOO['cedents']['succ']}")#line:1273
                print (f"  condition  : {O0OO0O0OOO0OO0OOO['cedents']['cond']}")#line:1274
                print (f"  first set  : {O0OO0O0OOO0OO0OOO['cedents']['frst']}")#line:1275
                print (f"  second set : {O0OO0O0OOO0OO0OOO['cedents']['scnd']}")#line:1276
                print ("")#line:1277
                print ("Fourfold tables:")#line:1278
                print (f"FRST|  S  |  ¬S |  SCND|  S  |  ¬S |");#line:1279
                print (f"----|-----|-----|  ----|-----|-----| ")#line:1280
                print (f" A  |{'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['fourfold1'][0])}|{'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['fourfold1'][1])}|   A  |{'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['fourfold2'][0])}|{'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['fourfold2'][1])}|")#line:1281
                print (f"----|-----|-----|  ----|-----|-----|")#line:1282
                print (f"¬A  |{'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['fourfold1'][2])}|{'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['fourfold1'][3])}|  ¬A  |{'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['fourfold2'][2])}|{'{:5d}'.format(O0OO0O0OOO0OO0OOO['params']['fourfold2'][3])}|")#line:1283
                print (f"----|-----|-----|  ----|-----|-----|")#line:1284
            else :#line:1285
                print ("Unsupported task type for rule details")#line:1286
            print ("")#line:1290
        else :#line:1291
            print ("No such rule.")#line:1292
