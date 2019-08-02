import operator
import re
import importlib

#Returns a dictionary with key being a feature and value being the weight
#Takes a 4 item tuple as an argument. [0]=current word [1]=previous word [2]=following word [3]=index number within sentence
def FeatureChecker(tup):
    d = {}

    #BIAS
    d["b_bias"] = 1.
    #Current token
    d["cw_"+tup[0]] = 1.
    #Current token suffix(3 chars)
    if len(tup[0]) >= 5:
        d["cw-suf_"+tup[0][-3:]] = 1.
    #Current token contains numerical character
    if re.search('[0-9]+', tup[0]):
        d["n_num"] = 1.
    #Previous token
    if tup[1] != "_NULL_" :
        d["pw_"+tup[1]] = 1.
    #Following token'
    if tup[2] != "_NULL_" :
        d["fw_"+tup[2]] = 1.
    #Index Number
    si = str(tup[3])
    d["ind_"+si] = 1.

#Linguistic Rule Based Features
#Common Word Sets
    #Prepositions https://www.englishclub.com/vocabulary/common-prepositions-25.htm
    prepositions = {"of","OF","Of","in","IN","In","to","TO","To","for","FOR","For","with","WITH","With","on","ON","On","at","AT","At","from","FROM","From","by","BY","By","about","ABOUT","About","as","AS","As","into","INTO","Into","like","LIKE","Like","through","THROUGH","Through","after","AFTER","After","over","OVER","Over","between","BETWEEN","Between","out","OUT","Out","against","AGAINST","Against","during","DURING","During","without","WITHOUT","Without","before","BEFORE","Before","under","UNDER","Under","around","AROUND","Around","among","AMONG","Among"}
    #Verbs to Be https://en.wikipedia.org/wiki/Copula_(linguistics)#English
    tobes = {"be","BE","Be","am","AM","Am","is","IS","Is","are","ARE","Are","being","BEING","Being","was","WAS","Was","were","WERE","Were","been","BEEN","been","\'s","\'S","\'re","\'RE"}
    #Modal Verbs https://www.myenglishpages.com/site_php_files/grammar-lesson-modals.php
    modals = {"can","CAN","Can","could","COULD","Could","may","MAY","May","might","MIGHT","Might","will","WILL","Will","would","WOULD","Would","shall","SHALL","Shall","should","SHOULD","Should","must","MUST","Must"}
    pastps = {"has","HAS","Has","have","HAVE","Have","had","HAD","Had","\'s","\'S","\'ve","\'VE","\'d","\'D"}
    whadverbs = {"who","WHO","Who","what","WHAT","What","where","WHERE","Where","when","WHEN","When","why","WHY","Why","how","HOW","How","whom","WHOM","Whom","whose","WHOSE","Whose"}
    #Pronouns https://www.english-grammar-revolution.com/list-of-pronouns.html
    pronouns = {"i","I","me","ME","Me","we","WE","We","us","US","Us","you","YOU","You","she","SHE","She","her","HER","her","he","HE","He","him","HIM","Him","it","IT","It","they","THEY","They","them","THEM","Them","that","THAT","That","which","WHICH","Which","who","WHO","Who","whom","WHOM","Whom","whose","WHOSE","Whose","whichever","WHICHEVER","Whichever","whoever","WHOEVER","Whoever","whomever","WHOMEVER","Whomever","this","THIS","This","that","THAT","That","these","THESE","These","those","THOSE","Those","myself","MYSELF","Myself","ourselves","OURSELVES","Ourselves","yourself","YOURSELF","Yourself","yourselves","YOURSELVES","Yourselves","himself","HIMSELF","Himself","herself","HERSELF","Herself","itself","ITSELF","Itself","themselves","THEMSELVES","Themselves"}
    indefs = {"anybody","ANYBODY","Anybody","anyone","ANYONE","Anyone","anything","ANYTHING","Anything","each","EACH","Each","either","EITHER","Either","everybody","EVERYBODY","Everybody","everyone","EVERYONE","Everyone","everything","EVERYTHING","Everything","neither","NEITHER","Neither","nobody","NOBODY","Nobody","nothing","NOTHING","Nothing","one","ONE","One","somebody","SOMEBODY","Somebody","someone","SOMEONE","Someone","something","SOMETHING","Something","both","BOTH","Both","few","FEW","Few","many","MANY","Many","several","SEVERAL","Several","all","ALL","All","any","ANY","Any","most","MOST","Most","none","NONE","None","some","SOME","Some"}
    possps = {"my","MY","My","your","YOUR","Your","his","HIS","His","her","HER","Her","its","ITS","Its","our","OUR","Our","your","YOUR","Your","their","THEIR","Their","mine","MINE","Mine","yours","YOURS","Yours","his","HIS","His","hers","HERS","Hers","ours","OURS","Ours","yours","YOURS","Yours","theirs","THEIRS","Theirs"}
    #Common adverbs including temporal ones https://www.ef.com/wwen/english-resources/english-grammar/adverbs-time/
    cadverbs = {"here","HERE","Here","there","THERE","There","where","WHERE","Where","then","THEN","Then","when","WHEN","When","later","LATER","Later","since","SINCE","Since","often","OFTEN","Often"}
    #Conjunctions https://www.english-grammar-revolution.com/list-of-conjunctions.html
    cconjs = {"for","FOR","Fore","and","AND","And","but","BUT","But","or","OR","Or","yet","YET","Yet","so","SO","So"}
    sconjs = {"after","AFTER","After","although","ALTHOUGH","Although","as","AS","As","because","BECAUSE","Because","before","BEFORE","Before", "even","EVEN","Even","if","IF","If","lest","LEST","Lest","once","ONCE","Once","since","SINCE","Since","than","THAN","Than","that","THAT","That","though","THOUGH","Though","till","TILL","Till","unless","UNLESS","Unless","until","UNTIL","Until","when","WHEN","When","whenever","WHENEVER","Whenever","where","WHERE","Where","wherever","WHEREVER","Wherever","while","WHILE","While"}
    negs = {"not","NOT","Not","n\'t","N\'T","never","NEVER","Never","no","NO","No","nor","NOR","nor","neither","NEITHER","Neither"}
    symbols = {"\'","\"","\\","/","$",".","?","!",",","<",">","=","(",")","[","]","{","}","@","#","%","^","&","*","-",";",":","|","+","_","~","`","``"}

#Lexical Features - i = "is" as in the word "is" this; b = "begins with"; e = "ends with"
#Inflectional Endings
    #eED
    if re.search('\S+[Ee][Dd]$', tup[0]) :
        d["eED"] = 1.
    #eIED
    if re.search('\S+[Ii][Ee][Dd]', tup[0]):
        d["eIED"] = 1.
    #eS
    if len(tup[0]) > 2 and re.search('\S+[Ss]$', tup[0]) :
        d["eS"] = 1.
    #eES
    if re.search('\S+[Ee][Ss]$', tup[0]) :
        d["eES"] = 1.
    #eIES
    if re.search('\S+[Ii][Ee][Ss]$', tup[0]) :
        d["eIES"] = 1.
    #eING
    if re.search('\S+[Ii][Nn][Gg]$', tup[0]) :
        d["eING"] = 1.
    #eINGS
    if re.search('\S+[Ii][Nn][Gg][Ss]$', tup[0]) :
        d["eINGS"] = 1.
    #eER
    if re.search('\S+[Ee][Rr]$', tup[0]) :
        d["eER"] = 1.
    #eERS
    if re.search('\S+[Ee][Rr][Ss]$', tup[0]) :
        d["eERS"] = 1.
    #eIER
    if re.search('\S+[Ii][Ee][Rr]$', tup[0]) :
        d["eIER"] = 1.
    #eIERS
    if re.search('\S+[Ii][Ee][Rr][Ss]$', tup[0]) :
        d["eIERS"] = 1.
    #eEST
    if re.search('\S+[Ee][Ss][Tt]$', tup[0]) :
        d["eEST"] = 1.
    #eESTS
    if re.search('\S+[Ee][Ss][Tt][Ss]$', tup[0]) :
        d["eESTS"] = 1.
    #eIEST
    if re.search('\S+iest$', tup[0]) or re.search('\S+IEST$', tup[0]) :
        d["eIEST"] = 1.
    #eIESTS
    if re.search('\S+[Ii][Ee][Ss][Tt][Ss]$', tup[0]) :
        d["eIESTS"] = 1.


#Nominalizations - http://usefulenglish.ru/writing/list-of-nouns-with-suffixes
    #eION
    if re.search('\S+[Ii][Oo][Nn]$', tup[0]) :
        d["eION"] = 1.
    #eIONS
    if re.search('\S+[Ii][Oo][Nn][Ss]$', tup[0]) :
        d["eIONS"] = 1.
    #eSION
    if re.search('\S+[Ss][Ii][Oo][Nn]$', tup[0]) :
        d["eSION"] = 1.
    #eSIONS
    if re.search('\S+[Ss][Ii][Oo][Nn][Ss]$', tup[0]) :
        d["eSIONS"] = 1.
    #eTION
    if re.search('\S+[Tt][Ii][Oo][Nn]$', tup[0]) :
        d["eTION"] = 1.
    #eTIONS
    if re.search('\S+[Tt][Ii][Oo][Nn][Ss]$', tup[0]) :
        d["eTIONS"] = 1.
    #eATION
    if re.search('\S+[Aa][Tt][Ii][Oo][Nn]$', tup[0]) :
        d["eATION"] = 1.
    #eATIONS
    if re.search('\S+[Aa][Tt][Ii][Oo][Nn][Ss]$', tup[0]) :
        d["eATIONS"] = 1.
    #eNESS
    if re.search('\S+[Nn][Ee][Ss][Ss]$', tup[0]) :
        d["eNESS"] = 1.
    #eNESSES
    if re.search('\S+[Nn][Ee][Ss][Ss][Ee][Ss]$', tup[0]) :
        d["eNESSES"] = 1.
    #eSHIP
    if re.search('\S+[Ss][Hh][Ii][Pp]$', tup[0]) :
        d["eSHIP"] = 1.
    #eSHIPS
    if re.search('\S+[Ss][Hh][Ii][Pp][Ss]$', tup[0]) :
        d["eSHIPS"] = 1.
    #eMENT
    if re.search('\S+[Mm][Ee][Nn][Tt]$', tup[0]) :
        d["eMENT"] = 1.
    #eMENTS
    if re.search('\S+[Mm][Ee][Nn][Tt][Ss]$', tup[0]) :
        d["eMENTS"] = 1.
    #eACY
    if re.search('\S+[Aa][Cc][Yy]$', tup[0]) :
        d["eACY"] = 1.
    #eACIES
    if re.search('\S+[Aa][Cc][Ii][Ee][Ss]$', tup[0]) :
        d["eACIES"] = 1.
    #eADE
    if len(tup[0]) > 4 and re.search('\S+[Aa][Dd][Ee]$', tup[0]) :
        d["eADE"] = 1.
    #eADES
    if len(tup[0]) > 5 and re.search('\S+[Aa][Dd][Ee][Ss]$', tup[0]) :
        d["eADES"] = 1.
    #eAGE
    if re.search('\S+[Aa][Gg][Ee]$', tup[0]) :
        d["eAGE"] = 1.
    #eAGES
    if re.search('\S+[Aa][Gg][Ee][Ss]$', tup[0]) :
        d["eAGES"] = 1.
    #eAN
    if len(tup[0]) > 3 and re.search('\S+[Aa][Nn]$', tup[0]) :
        d["eAN"] = 1.
    #eANS
    if len(tup[0]) > 4 and re.search('\S+[Aa][Nn][Ss]$', tup[0]) :
        d["eANS"] = 1.
    #eIAN
    if re.search('\S+[Ii][Aa][Nn]$', tup[0]) :
        d["eIAN"] = 1.
    #eIANS
    if re.search('\S+[Ii][Aa][Nn][Ss]$', tup[0]) :
        d["eIANS"] = 1.
    #eDOM
    if re.search('\S+[Dd][Oo][Mm]$', tup[0]) :
        d["eDOM"] = 1.
    #eDOMS
    if re.search('\S+[Dd][Oo][Mm][Ss]$', tup[0]) :
        d["eDOMS"] = 1.
    #eET
    if len(tup[0]) > 5 and re.search('\S+[Ee][Tt]$', tup[0]) :
        d["eET"] = 1.
    #eETS
    if len(tup[0]) > 6 and re.search('\S+[Ee][Tt][Ss]$', tup[0]) :
        d["eETS"] = 1.
    #eETTE
    if re.search('\S+[Ee][Tt][Tt][Ee]$', tup[0]) :
        d["eETTE"] = 1.
    #eETTES
    if re.search('\S+[Ee][Tt][Tt][Ee][Ss]$', tup[0]) :
        d["eETTES"] = 1.
    #eLET
    if len(tup[0]) > 4 and re.search('\S+[Ll][Ee][Tt]$', tup[0]) :
        d["eLET"] = 1.
    #eLETS
    if len(tup[0]) > 5 and re.search('\S+[Ll][Ee][Tt][Ss]$', tup[0]) :
        d["eLETS"] = 1.
    #eHOOD
    if re.search('\S+[Hh][Oo][Oo][Dd]$', tup[0]) :
        d["eHOOD"] = 1.
    #eHOODS
    if re.search('\S+[Hh][Oo][Oo][Dd][Ss]$', tup[0]) :
        d["eHOODS"] = 1.
    #eICE
    if re.search('\S+[Ii][Cc][Ee]$', tup[0]) :
        d["eICE"] = 1.
    #eICES
    if re.search('\S+[Ii][Cc][Ee][Ss]$', tup[0]) :
        d["eICE"] = 1.
    #eIN
    if len(tup[0]) > 4 and re.search('\S+[Ii][Nn]$', tup[0]) :
        d["eIN"] = 1.
    #eINS
    if len(tup[0]) > 5 and re.search('\S+[Ii][Nn][Ss]$', tup[0]) :
        d["eINS"] = 1.
    #eINE
    if re.search('\S+[Ii][Nn][Ee]$', tup[0]) :
        d["eINE"] = 1.
    #eINES
    if re.search('\S+[Ii][Nn][Ee][Ss]$', tup[0]) :
        d["eINES"] = 1.
    #eISM
    if re.search('\S+[Ii][Ss][Mm]$', tup[0]) :
        d["eISM"] = 1.
    #eISMS
    if re.search('\S+[Ii][Ss][Mm][Ss]$', tup[0]) :
        d["eISMS"] = 1.
    #eIST
    if re.search('\S+[Ii][Ss][Tt]$', tup[0]) :
        d["eIST"] = 1.
    #eISTS
    if re.search('\S+[Ii][Ss][Tt][Ss]$', tup[0]) :
        d["eISTS"] = 1.
    #eIVE
    if len(tup[0]) > 5 and re.search('\S+[Ii][Vv][Ee]$', tup[0]) :
        d["eIVE"] = 1.
    #eIVES
    if len(tup[0]) > 6 and re.search('\S+[Ii][Vv][Ee][Ss]$', tup[0]) :
        d["eIVES"] = 1.
    #eTUDE
    if re.search('\S+[Tt][Uu][Dd][Ee]$', tup[0]) :
        d["eTUDE"] = 1.
    #eTUDES
    if re.search('\S+[Tt][Uu][Dd][Ee][Ss]$', tup[0]) :
        d["eTUDES"] = 1.
    #eURE
    if re.search('\S+[Uu][Rr][Ee]$', tup[0]) :
        d["eURES"] = 1.
    #eURES
    if re.search('\S+[Uu][Rr][Ee][Ss]$', tup[0]) :
        d["eURES"] = 1.
    #eANCE
    if re.search('\S+[Aa][Nn][Cc][Ee]$', tup[0]) :
        d["eANCE"] = 1.
    #eANCES
    if re.search('\S+[Aa][Nn][Cc][Ee][Ss]$', tup[0]) :
        d["eANCES"] = 1.
    #eENCE
    if re.search('\S+[Ee][Nn][Cc][Ee]$', tup[0]) :
        d["eENCE"] = 1.
    #eENCES
    if re.search('\S+[Ee][Nn][Cc][Ee][Ss]$', tup[0]) :
        d["eENCES"] = 1.
    #eANCY
    if re.search('\S+[Aa][Nn][Cc][Yy]$', tup[0]) :
        d["eANCY"] = 1.
    #eANCIES
    if re.search('\S+[Aa][Nn][Cc][Ii][Ee][Ss]$', tup[0]) :
        d["eANCIES"] = 1.
    #eENCY
    if re.search('\S+[Ee][Nn][Cc][Yy]$', tup[0]) :
        d["eENCY"] = 1.
    #eENCIES
    if re.search('\S+[Ee][Nn][Cc][Ii][Ee][Ss]$', tup[0]) :
        d["eENCIES"] = 1.
    #eENCE
    if re.search('\S+[Ee][Nn][Cc][Ee]$', tup[0]) :
        d["eENCE"] = 1.
    #eENCES
    if re.search('\S+[Ee][Nn][Cc][Ee][Ss]$', tup[0]) :
        d["eENCES"] = 1.
    #eANT
    if re.search('\S+[Aa][Nn][Tt]$', tup[0]) :
        d["eANT"] = 1.
    #eANTS
    if re.search('\S+[Aa][Nn][Tt][Ss]$', tup[0]) :
        d["eANTS"] = 1.
    #eENT
    if re.search('\S+[Ee][Nn][Tt]$', tup[0]) :
        d["eENT"] = 1.
    #eENTS
    if re.search('\S+[Ee][Nn][Tt][Ss]$', tup[0]) :
        d["eENTS"] = 1.
    #eARY
    if re.search('\S+[Aa][Rr][Yy]$', tup[0]) :
        d["eARY"] = 1.
    #eARIES
    if re.search('\S+[Aa][Rr][Ii][Ee][Ss]$', tup[0]) :
        d["eARIES"] = 1.
    #eERY
    if re.search('\S+[Ee][Rr][Yy]$', tup[0]) :
        d["eERY"] = 1.
    #eERIES
    if re.search('\S+[Ee][Rr][Ii][Ee][Ss]$', tup[0]) :
        d["eERIES"] = 1.
    #eORY
    if re.search('\S+[Oo][Rr][Yy]$', tup[0]) :
        d["eORY"] = 1.
    #eORIES
    if re.search('\S+[Oo][Rr][Ii][Ee][Ss]$', tup[0]) :
        d["eORIES"] = 1.
    #eOR
    if re.search('\S+[Oo][Rr]$', tup[0]) :
        d["eOR"] = 1.
    #eORS
    if re.search('\S+[Oo][Rr][Ss]$', tup[0]) :
        d["eORS"] = 1.
    #eEER
    if re.search('\S+[Ee][Ee][Rr]$', tup[0]) :
        d["eEER"] = 1.
    #eEERS
    if re.search('\S+[Ee][Ee][Rr][Ss]$', tup[0]) :
        d["eEERS"] = 1.
    #eEE
    if len(tup[0]) > 3 and re.search('\S+[Ee][Ee]$', tup[0]) :
        d["eEE"] = 1.
    #eEES
    if len(tup[0]) > 4 and re.search('\S+[Ee][Ee][Ss]$', tup[0]) :
        d["eEES"] = 1.
    #eESS
    if re.search('\S+[Ee][Ss][Ss]$', tup[0]) :
        d["eESS"] = 1.
    #eESSES
    if re.search('\S+[Ee][Ss][Ss][Ee][Ss]$', tup[0]) :
        d["eESSES"] = 1.
    #eTY
    if re.search('\S+[Tt][Yy]$', tup[0]) :
        d["eTY"] = 1.
    #eTIES
    if re.search('\S+[Tt][Ii][Ee][Ss]$', tup[0]) :
        d["eTIES"] = 1.
    #eITY
    if re.search('\S+[Ii][Tt][Yy]$', tup[0]) :
        d["eITY"] = 1.
    #eITIES
    if re.search('\S+[Ii][Tt][Ii][Ee][Ss]$', tup[0]) :
        d["eITIES"] = 1.
    #eSELF
    if re.search('\S+[Ss][Ee][Ll][Ff]$', tup[0]) :
        d["eSELF"] = 1.
    #eSELVES
    if re.search('\S+[Ss][Ee][Ll][Vv][Ee][Ss]$', tup[0]) :
        d["eSELVES"] = 1.

#Verbification - http://usefulenglish.ru/writing/list-of-verbs-with-suffixes
    #eATE
    if re.search('\S+[Aa][Tt][Ee]$', tup[0]) :
        d["eATE"] = 1.
    #eATES
    if re.search('\S+[Aa][Tt][Ee][Ss]$', tup[0]) :
        d["eATES"] = 1.
    #eATED
    if re.search('\S+[Aa][Tt][Ee][Dd]$', tup[0]) :
        d["eATED"] = 1.
    #eATING
    if re.search('\S+[Aa][Tt][Ii][Nn][Gg]$', tup[0]) :
        d["eATING"] = 1.
    #eATINGS
    if re.search('\S+[Aa][Tt][Ii][Nn][Gg]$', tup[0]) :
        d["eATINGS"] = 1.
    #eEN
    if len(tup[0]) > 4 and re.search('\S+[Ee][Nn]$', tup[0]) :
        d["eEN"] = 1.
    #eENS
    if len(tup[0]) > 4 and re.search('\S+[Ee][Nn][Ss]$', tup[0]) :
        d["eENS"] = 1.
    #eENED
    if re.search('\S+[Ee][Nn][Ee][Dd]$', tup[0]) :
        d["eENED"] = 1.
    #eENING
    if re.search('\S+[Ee][Nn][Ii][Nn][Gg]$', tup[0]) :
        d["eENING"] = 1.
    #eENINGS
    if re.search('\S+[Ee][Nn][Ii][Nn][Gg]$', tup[0]) :
        d["dENINGS"] = 1.
    #eFY
    if re.search('\S+[Ff][Yy]$', tup[0]) :
        d["eFY"] = 1.
    #eFIES
    if re.search('\S+[Ff][Ii][Ee][Ss]$', tup[0]) :
        d["eFIES"] = 1.
    #eFIED
    if re.search('\S+[Ff][Ii][Ee][Dd]$', tup[0]) :
        d["eFIED"] = 1.
    #eFYING
    if re.search('\S+[Ff][Yy][Ii][Nn][Gg]$', tup[0]) :
        d["eFYING"] = 1.
    #eFYINGS
    if re.search('\S+[Ff][Yy][Ii][Nn][Gg][Ss]$', tup[0]) :
        d["eFYINGS"] = 1.
    #eIFY
    if re.search('\S+[Ii][Ff][Yy]$', tup[0]) :
        d["eIFY"] = 1.
    #eIFIES
    if re.search('\S+[Ii][Ff][Ii][Ee][Ss]$', tup[0]) :
        d["eIFIES"] = 1.
    #eIFIED
    if re.search('\S+[Ii][Ff][Ii][Ee][Dd]$', tup[0]) :
        d["eIFIED"] = 1.
    #eIFYING
    if re.search('\S+[Ii][Ff][Yy][Ii][Nn][Gg]$', tup[0]) :
        d["eIFYING"] = 1.
    #eIFYINGS
    if re.search('\S+[Ii][Ff][Yy][Ii][Nn][Gg][Ss]$', tup[0]) :
        d["eIFYINGS"] = 1.
    #eEFY
    if re.search('\S+[Ee][Ff][Yy]$', tup[0]) :
        d["eEFY"] = 1.
    #eEFIES
    if re.search('\S+[Ee][Ff][Ii][Ee][Ss]$', tup[0]) :
        d["eEFIES"] = 1.
    #eEFIED
    if re.search('\S+[Ee][Ff][Ii][Ee][Dd]$', tup[0]) :
        d["eEFIED"] = .1
    #eEFYING
    if re.search('\S+[Ee][Ff][Yy][Ii][Nn][Gg]$', tup[0]) :
        d["eEFYING"] = 1.
    #eEFYINGS
    if re.search('\S+[Ee][Ff][Yy][Ii][Nn][Gg][Ss]$', tup[0]) :
        d["eEFYINGS"] = 1.
    #eISH
    if re.search('\S+[Ii][Ss][Hh]$', tup[0]) :
        d["eISH"] = 1.
    #eISHES
    if re.search('\S+[Ii][Ss][Hh][Ee][Ss]$', tup[0]) :
        d["eISHES"] = 1.
    #eISHED
    if re.search('\S+[Ii][Ss][Hh][Ee][Dd]$', tup[0]) :
        d["eISHED"] = 1.
    #eISHING
    if re.search('\S+[Ii][Ss][Hh][Ii][Nn][Gg]$', tup[0]) :
        d["eISHING"] = 1.
    #eISHINGS
    if re.search('\S+[Ii][Ss][Hh][Ii][Nn][Gg][Ss]$', tup[0]) :
        d["eISHINGS"] = 1.
    #eIZE (also includes British English "ise" for all subsequent "ize" endings)
    if len(tup[0]) > 5 and re.search('\S+[Ii][SsZz][Ee]$', tup[0]) :
        d["eIZE"] = 1.
    #eIZES
    if len(tup[0]) > 5 and re.search('\S+[Ii][SsZz][Ee][Ss]$', tup[0]) :
        d["eIZES"] = 1.
    #eIZED
    if len(tup[0]) > 5 and re.search('\S+[Ii][SsZz][Ee][Dd]$', tup[0]) :
        d["eIZED"] = 1.
    #eIZING
    if len(tup[0]) > 5 and re.search('\S+[Ii][SsZz][Ii][Nn][Gg]$', tup[0]) :
        d["eIZING"] = 1.
    #eIZINGS
    if len(tup[0]) > 5 and re.search('\S+[Ii][SsZz][Ii][Nn][Gg][Ss]$', tup[0]) :
        d["eIZINGS"] = 1.

#Adjectivication - http://usefulenglish.ru/writing/list-of-derivative-adjectives
    #eFUL
    if re.search('\S+[Ff][Uu][Ll]$', tup[0]) :
        d["eFUL"] = 1.
    #eIC
    if re.search('\S+[Ii][Cc]$', tup[0]) :
        d["eIC"] = 1.
    #eICS
    if re.search('\S+[Ii][Cc][Ss]$', tup[0]) :
        d["eICS"] = 1.
    #eTIC
    if re.search('\S+[Tt][Ii][Cc]$', tup[0]) :
        d["eTIC"] = 1.
    #eTICS
    if re.search('\S+[Tt][Ii][Cc][Ss]$', tup[0]) :
        d["eTICS"] = 1.
    #eABLE
    if re.search('\S+[Aa][Bb][Ll][Ee]$', tup[0]) :
        d["eABLE"] = 1.
    #eABLES
    if re.search('\S+[Aa][Bb][Ll][Ee][Ss]$', tup[0]) :
        d["eABLES"] = 1.
    #eIBLE
    if re.search('\S+[Ii][Bb][Ll][Ee]$', tup[0]) :
        d["eIBLE"] = 1.
    #eIBLES
    if re.search('\S+[Ii][Bb][Ll][Ee][Ss]$', tup[0]) :
        d["eIBLES"] = 1.
    #eAL
    if re.search('\S+[Aa][Ll]$', tup[0]) :
        d["eAL"] = 1.
    #eALS
    if re.search('\S+[Aa][Ll][Ss]$', tup[0]) :
        d["eALS"] = 1.
    #eIAL
    if re.search('\S+[Ii][Aa][Ll]$', tup[0]) :
        d["eIAL"] = 1.
    #eIALS
    if re.search('\S+[Ii][Aa][Ll][Ss]$', tup[0]) :
        d["eIALS"] = 1.


#Adverbification - http://usefulenglish.ru/writing/list-of-adverbs
    #eLY
    if re.search('\S+[Ll][Yy]$', tup[0]) :
        d["eLY"] = 1.
    #eWARD
    if re.search('\S[Ww][Aa][Rr][Dd]$', tup[0]) :
        d["eWARD"] = 1.
    #eWARDS
    if re.search('\S[Ww][Aa][Rr][Dd][Ss]$', tup[0]) :
        d["eWARDS"] = 1.
    #eWAYS
    if re.search('\S[Ww][Aa][Yy][Ss]$', tup[0]) :
        d["eWAYS"] = 1.
    #eWISE
    if re.search('\S[Ww][Ii][Ss][Ee]$', tup[0]) :
        d["eWISE"] = 1.

#Prefixes - For short prefixes(3 or less letters), rules include a word length greater than 6
# http://usefulenglish.ru/writing/prefixes-meanings-examples
    #bANTI
    if re.search('^[Aa][Nn][Tt][Ii]\S+', tup[0]) :
        d["bANTI"] = 1.
    #bAUTO
    if re.search('^[Aa][Uu][Tt][Oo]\S+', tup[0]) :
        d["bAUTO"] = 1.
    #bCOM
    if len(tup[0]) > 6 and re.search('^[Cc][Oo][Mm]\S+', tup[0]) :
        d["bCOM"] = 1.
    #bCON
    if len(tup[0]) > 6 and re.search('^[Cc][Oo][Nn]\S+', tup[0]) :
        d["bCON"] = 1.
    #bDIS
    if len(tup[0]) > 6 and re.search('^[Dd][Ii][Ss]\S+', tup[0]) :
        d["bDIS"] = 1.
    #bDYS
    if len(tup[0]) > 6 and re.search('^[Dd][Yy][Ss]\S+', tup[0]) :
        d["bDYS"] = 1.
    #bEM
    if len(tup[0]) > 6 and re.search('^[Ee][Mm]\S+', tup[0]) :
        d["bEM"] = 1.
    #bEN
    if len(tup[0]) > 6 and re.search('^[Ee][Nn]\S+', tup[0]) :
        d["bEN"] = 1.
    #bEX
    if len(tup[0]) > 6 and re.search('^[Ee][Xx]\S+', tup[0]) :
        d["bEX"] = 1.
    #bEXTR
    if re.search('^[Ee][Xx][Tt][Rr]\S+', tup[0]) :
        d["bEXTR"] = 1.
    #bFOR
    if len(tup[0]) > 6 and re.search('^[Ff][Oo][Rr]\S+', tup[0]) :
        d["bFOR"] = 1.
    #bHYPER
    if re.search('^[Hh][Yy][Pp][Ee][Rr]\S+', tup[0]) :
        d["bHYPER"] = 1.
    #bHYPO
    if re.search('^[Hh][Yy][Pp][Oo]\S+', tup[0]) :
        d["bHYPO"] = 1.
    #bIN
    if len(tup[0]) > 6 and re.search('^[Ii][Nn]\S+', tup[0]) :
        d["bIN"] = 1.
    #bINTER
    if re.search('^[Ii][Nn][Tt][Ee][Rr]\S+', tup[0]) :
        d["bINTER"] = 1.
    #bINTRA
    if re.search('^[Ii][Nn][Tt][Rr][Aa]\S+', tup[0]) :
        d["bINTRA"] = 1.
    #bMICRO
    if re.search('^[Mm][Ii][Cc][Rr][Oo]\S+', tup[0]) :
        d["bMICRO"] = 1.
    #bMID
    if len(tup[0]) > 6 and re.search('^[Mm][Ii][Dd]\S+', tup[0]) :
        d["bMID"] = 1.
    #bMIS
    if len(tup[0]) > 6 and re.search('^[Mm][Ii][Ss]\S+', tup[0]) :
        d["bMIS"] = 1.
    #bMULTI
    if re.search('^[Mm][Uu][Ll][Tt][Ii]\S+', tup[0]) :
        d["bMULTI"] = 1.
    #bNON
    if len(tup[0]) > 6 and re.search('^[Nn][Oo][Nn]\S+', tup[0]) :
        d["bNON"] = 1.
    #bOB
    if len(tup[0]) > 6 and re.search('^[Oo][Bb]\S+', tup[0]) :
        d["bOB"] = 1.
    #bOFF
    if len(tup[0]) > 6 and re.search('^[Oo][Ff][Ff]\S+', tup[0]) :
        d["bOFF"] = 1.
    #bON
    if len(tup[0]) > 6 and re.search('^[Oo][Nn]\S+', tup[0]) :
        d["bON"] = 1.
    #bOUT
    if len(tup[0]) > 6 and re.search('^[Oo][Uu][Tt]\S+', tup[0]) :
        d["bOUT"] = 1.
    #bOVER
    if re.search('^[Oo][Vv][Ee][Rr]\S+', tup[0]) :
        d["bOVER"] = 1.
    #bPARA
    if len(tup[0]) > 6 and re.search('^[Pp][Aa][Rr][Aa]\S+', tup[0]) :
        d["bPARA"] = 1.
    #bPER
    if len(tup[0]) > 6 and re.search('^[Pp][Ee][Rr]\S+', tup[0]) :
        d["bPER"] = 1.
    #bPOST
    if len(tup[0]) > 6 and re.search('^[Pp][Oo][Ss][Tt]\S+', tup[0]) :
        d["bPOST"] = 1.
    #bPRE
    if len(tup[0]) > 6 and re.search('^[Pp][Rr][Ee]\S+', tup[0]) :
        d["bPRE"] = 1.
    #bPRO
    if len(tup[0]) > 6 and re.search('^[Pp][Rr][Oo]\S+', tup[0]) :
        d["bPRO"] = 1.
    #bRE
    if len(tup[0]) > 6 and re.search('^[Rr][Ee]\S+', tup[0]) :
        d["bRE"] = 1.
    #bSELF
    if re.search('^[Ss][Ee][Ll][Ff]\S+', tup[0]) :
        d["bSELF"] = 1.
    #bSUB
    if len(tup[0]) > 6 and re.search('^[Ss][Uu][Bb]\S+', tup[0]) :
        d["bSUB"] = 1.
    #bSUP
    if len(tup[0]) > 6 and re.search('^[Ss][Uu][Pp]\S+', tup[0]) :
        d["bSUP"] = 1.
    #bSUR
    if len(tup[0]) > 6 and re.search('^[Ss][Uu][Rr]\S+', tup[0]) :
        d["bSUR"] = 1.
    #bTRANS
    if re.search('^[Tt][Rr][Aa][Nn][Ss]\S+', tup[0]) :
        d["bTRANS"] = 1.
    #bUN
    if len(tup[0]) > 6 and re.search('^[Uu][Nn]\S+', tup[0]) :
        d["bUN"] = 1.
    #bUNDER
    if re.search('^[Uu][Nn][Dd][Ee][Rr]\S+', tup[0]) :
        d["bUNDER"] = 1.
    #bUNI
    if len(tup[0]) > 6 and re.search('^[Uu][Nn][Ii]\S+', tup[0]) :
        d["bUNI"] = 1.
    #bUP
    if len(tup[0]) > 6 and re.search('^[Uu][Pp]\S+', tup[0]) :
        d["bUP"] = 1.
    #bWITH
    if re.search('^[Ww][Ii][Tt][Hh]\S+', tup[0]) :
        d["bWITH"] = 1.

#Other
    #bCAP
    if re.search('^[A-Z]', tup[0]) :
        d["bCAP"] = 1.
    #bAPOS
    if re.search('^\'', tup[0]) :
        d["bAPOS"] = 1.
    #iG7
    if len(tup[0]) > 7 :
        d["iG7"] = 1.
    #iSYM
    if tup[0] in symbols :
        d["iSYM"] = 1.

#Context Features - p = "previous token is"; f = "following token is"
#prepositions;tobes;modals;pastps;whadverbs;pronouns;indefs;possps;cadverbs;cconjs;sconjs;negs;symbols
#Previous Word
    if tup[1] != "_NULL_" :
        #pPREP - Previous token is a preposition
        if tup[1] in prepositions :
            d["pPREP"] = 1.
        #pTOBE - Previous token is a form of the verb "to be"
        if tup[1] in tobes :
            d["pTOBE"] = 1.
        #pMOD - Previous token is a modal verb
        if tup[1] in modals :
            d["pMOD"] = 1.
        #pPASTP - Previous token is a past participle/perfect
        if tup[1] in pastps :
            d["pPASTP"] = 1.
        #pWH - Previous token is a WH adverb
        if tup[1] in whadverbs :
            d["pWH"] = 1.
        #pPRO - Previous token is a pronoun (excluding indefinite and possesive pronouns)
        if tup[1] in pronouns :
            d["pPRO"] = 1.
        #pINDEF - Previous token is an indefinite pronoun
        if tup[1] in indefs :
            d["pINDEF"] = 1.
        #pPOSP - Previous token is a possesive pronoun
        if tup[1] in possps :
            d["pPOSP"] = 1.
        #pADV - Previous token is a common - mostly temporal - adverb
        if tup[1] in cadverbs :
            d["pPRO"] = 1.
        #pCCONJ - Previous token is a coordinating conjuntion
        if tup[1] in cconjs :
            d["pCCONJ"] = 1.
        #pSCONJ - Previous token is a subordinating conjunction
        if tup[1] in sconjs :
            d["pSCONJ"] = 1.
        #pNEG - Previous token is a word of negation
        if tup[1] in negs :
            d["pNEG"] = 1.
        #pSYM - Previous token is a symbol
        if tup[1] in symbols :
            d["pSYM"] = 1.

#Following Word
    if tup[2] != "_NULL_" :
        #fPREP - Following token is a preposition
        if tup[2] in prepositions :
            d["fPREP"] = 1.
        #fTOBE - Following token is a form of the verb "to be"
        if tup[2] in tobes :
            d["fTOBE"] = 1.
        #fMOD - Following token is a modal verb
        if tup[2] in modals :
            d["fMOD"] = 1.
        #fPASTP - Following token is a past participle/perfect
        if tup[2] in pastps :
            d["fPASTP"] = 1.
        #fWH - Following token is a WH adverb
        if tup[2] in whadverbs :
            d["fWH"] = 1.
        #fPRO - Following token is a pronoun (excluding indefinite and possesive pronouns)
        if tup[2] in pronouns :
            d["fPRO"] = 1.
        #fINDEF - Following token is an indefinite pronoun
        if tup[2] in indefs :
            d["fINDEF"] = 1.
        #fPOSP - Following token is a possesive pronoun
        if tup[2] in possps :
            d["fPOSP"] = 1.
        #fADV - Following token is a common - mostly temporal - adverb
        if tup[2] in cadverbs :
            d["fPRO"] = 1.
        #fCCONJ - Following token is a coordinating conjuntion
        if tup[2] in cconjs :
            d["fCCONJ"] = 1.
        #fSCONJ - Following token is a subordinating conjunction
        if tup[2] in sconjs :
            d["fSCONJ"] = 1.
        #fNEG - Following token is a word of negation
        if tup[1] in negs :
            d["fNEG"] = 1.
        #fSYM - Following token is a symbol
        if tup[2] in symbols :
            d["fSYM"] = 1.

    return d


#Returns a readable version of the gold data, a list of lists with [0] being the token and [1] being the POS
#Argument is a text file that breaks down into a list of strings
def GoldData(datafile) :
    golddata = []
    tokens = []
    POS = []
    for line in datafile:
        if line == "\n" :
            tokens.append(line)
            POS.append(line)
        else :
            stripped = line.strip()
            word = re.findall('(^\S*?)\s', stripped)[0]
            tag = re.findall('\s(\S*?$)', stripped)[0]
            tokens.append(word)
            POS.append(tag)
    golddata.append(tokens)
    golddata.append(POS)
    return golddata

#Returns a list of lists with each list representing a whole sentence
#Argument is a list of strings
def SenList(tokenlist) :
    allsentences = []
    sentence = []
    for word in tokenlist :
        if word == "\n" :
            allsentences.append(sentence)
            allsentences.append(word)
            sentence = []
        else :
            sentence.append(word)
    return allsentences

#Returns a list of tuples where [0] is the main token, [1] is the previous word, [2] is the following word, [3] is the index number within the sentence, and [4] is the gold data POS
#Argument is a list of lists with sentences
def PrevAndFoll(sentences,gpos) :
    pandf = list()
    for sent in sentences :
        if len(sent) == 1 :
            if sent[0] == "\n" :
                pandf.append(sent[0])
                gtag = gpos.pop(0)
            else :
                gtag = gpos.pop(0)
                a = (sent[0], "_NULL_", "_NULL_", "0", gtag)
                pandf.append(a)
                ind += 1
        else :
            ind = 0
            indmax = len(sent) - 1
            for word in sent :
                if ind == 0 :
                    gtag = gpos.pop(0)
                    a = (word, "_NULL_", sent[1], str(ind), gtag)
                    pandf.append(a)
                    ind += 1
                elif ind == indmax :
                    gtag = gpos.pop(0)
                    pind = indmax - 1
                    a = (word, sent[pind], "_NULL_", str(ind), gtag)
                    pandf.append(a)
                else :
                    gtag = gpos.pop(0)
                    pind = ind - 1
                    find = ind + 1
                    a = (word, sent[pind], sent[find], str(ind), gtag)
                    pandf.append(a)
                    ind += 1
    return pandf

#Built based on: https://towardsdatascience.com/6-steps-to-write-any-machine-learning-algorithm-from-scratch-perceptron-case-study-335f638a70f3
def Perceptron(feature,result,activation=0.0,learning_rate=0.1,epochs=23):
    #weight dict consisting of feature:weight pairs
    w = {}

    for e in range(0,epochs):
        for n in range(0,len(feature)):
            #f = calculated dot product of weights and features(input)

            f = 0.
            for k,v in feature[n].items():
                if k not in w:
                    w[k] = 0.
                f += w[k]*v

            #triggers activation function if f > activation
            if f > activation:
                yhat = 1.
            else:
                yhat = 0.

            #adapt weights only for current active features
            for k in feature[n]:
                w[k] = w[k] + learning_rate*(result[n] - yhat)*feature[n][k]

    return w

# train perceptron
# output = trained weights for each pos
def train(file,pandf):
    #get all pos of train dataset
    unique_pos = set()
    with open(file) as f:
        for l in f:
            if l != "\n":
                pos = l.split("\t")[1].strip()
                unique_pos.add(pos)

    result = {}
    for p in unique_pos:
        result[p] = [[],[]]
    prog = 0
    for tok in pandf :
        prog += 1
        print("learning @ line ",prog)
        if tok[0] != "\n" :
            for k,v in result.items() :
                featcheck = FeatureChecker(tok)
                if k == tok[4] :
                    result.get(k)[0].append(featcheck)
                    result.get(k)[1].append(1.)
                else:
                    result.get(k)[0].append(featcheck)
                    result.get(k)[1].append(0.)
    print("Training features checked")
    progress_count = 1
    #calculate perceptron weights
    for k,v in result.items():
        print("calculating perceptron "+str(progress_count)+"/"+str(len(result)))
        progress_count += 1
        result[k] = Perceptron(result.get(k)[0],result.get(k)[1])

    return result

def predict(file,pos_weights):
    devtext = open(file)
    gdata = GoldData(devtext)
    nopos = gdata[0]
    tagsonly = gdata[1]
    sentences = SenList(nopos)
    preandfol = PrevAndFoll(sentences,tagsonly)
    progress_count = 1
    predict_dataset = open(file,"r")
    out = open("RulePerceptronPredicted-"+file,"w")

    sentences = []
    sent_tmp = []

    #read file to be predicted
    for line in predict_dataset:
        token = line.split("\t")[0]
        if token != "\n":
            sent_tmp.append(token)
        if token == "\n":
            sentences.append(sent_tmp)
            sent_tmp = []

    progress_count = 0
    for i in range(0,len(sentences)):
        for j in range(0,len(sentences[i])):
            if preandfol[0] == "\n" :
                junk = preandfol.pop(0)
            tup = preandfol.pop(0)
            print("predicting @line: "+str(progress_count))
            progress_count += 1
            #we store the results of the dot product (weight + cur features)
            #in multi_class and the corresponding pos tag in multi_class_pos
            multi_class = []
            multi_class_pos = []
            for pos,weight in pos_weights.items():
                dot = 0.
                if j >= 1:
                    current_feat = FeatureChecker(tup)
                else:
                    current_feat = FeatureChecker(tup)

                #compute the dot product
                for k,v in current_feat.items():
                    if k in weight:
                        dot += v*weight[k]

                multi_class.append(dot)
                multi_class_pos.append(pos)
            #get the highest result (strongest weights) --> pos
            index,value = max(enumerate(multi_class),key=operator.itemgetter(1))
            out.write(sentences[i][j]+"\t"+multi_class_pos[index]+"\n")
        out.write("\n")
    out.close()

if __name__ == "__main__":
    tpath = "train.col"
    dpath = "test.col"
    devtext = open(tpath)
    golddata = GoldData(devtext)
    devtext.close()
    del devtext
    noposlist = golddata[0]
    justtags = golddata[1]
    sentences = SenList(noposlist)
    preandfol = PrevAndFoll(sentences,justtags)
    pos_weight = train(tpath, preandfol)
    predict(dpath,pos_weight)
