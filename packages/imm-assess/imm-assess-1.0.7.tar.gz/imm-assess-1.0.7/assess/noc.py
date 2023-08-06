import argparse
from termcolor import colored
from utils import utils
import enchant
import requests


noc_information='''

noc_infor:
   md: main duties
   tt: title
   te: title examples
   gd: general description
   er: employment requirements
   ai: additional information
   ec: exclusion 
   all: for all information
'''

# Version 2016 V1 NOC list
noc_list = ['0011', '0012', '0013', '0014', '0015', '0016', '0111', '0112', '0113', '0114', '0121', '0122', '0124', '0125', '0131', '0132', '0211', '0212', '0213', '0311', '0411', '0412', '0413', '0414', '0421', '0422', '0423', '0431', '0432', '0433', '0511', '0512', '0513', '0601', '0621', '0631', '0632', '0651', '0711', '0712', '0714', '0731', '0811', '0821', '0822', '0823', '0911', '0912', '1111', '1112', '1113', '1114', '1121', '1122', '1123', '1211', '1212', '1213', '1214', '1215', '1221', '1222', '1223', '1224', '1225', '1226', '1227', '1228', '1241', '1242', '1243', '1251', '1252', '1253', '1254', '1311', '1312', '1313', '1314', '1315', '1411', '1414', '1415', '1416', '1422', '1423', '1431', '1432', '1434', '1435', '1451', '1452', '1454', '1511', '1512', '1513', '1521', '1522', '1523', '1524', '1525', '1526', '2111', '2112', '2113', '2114', '2115', '2121', '2122', '2123', '2131', '2132', '2133', '2134', '2141', '2142', '2143', '2144', '2145', '2146', '2147', '2148', '2151', '2152', '2153', '2154', '2161', '2171', '2172', '2173', '2174', '2175', '2211',
            '2212', '2221', '2222', '2223', '2224', '2225', '2231', '2232', '2233', '2234', '2241', '2242', '2243', '2244', '2251', '2252', '2253', '2254', '2255', '2261', '2262', '2263', '2264', '2271', '2272', '2273', '2274', '2275', '2281', '2282', '2283', '3011', '3012', '3111', '3112', '3113', '3114', '3121', '3122', '3124', '3125', '3131', '3132', '3141', '3142', '3143', '3144', '3211', '3212', '3213', '3214', '3215', '3216', '3217', '3219', '3221', '3222', '3223',
            '3231', '3232', '3233', '3234', '3236', '3237', '3411', '3413', '3414', '4011', '4012', '4021', '4031', '4032', '4033', '4111', '4112', '4151', '4152', '4153', '4154', '4155', '4156', '4161', '4162', '4163', '4164', '4165', '4166', '4167', '4168', '4169', '4211', '4212', '4214', '4215', '4216', '4217', '4311', '4312', '4313', '4411', '4412', '4413', '4421', '4422', '4423', '5111', '5112', '5113', '5121', '5122', '5123','5124', '5125', '5131', '5132', '5133', '5134', '5135', '5136', '5211', '5212', '5221', '5222', '5223', '5224', '5225', '5226', '5227', '5231', '5232', '5241', '5242', '5243', '5244', '5245', '5251', '5252', '5253', '5254', '6211', '6221', '6222', '6231', '6232', '6235', '6311', '6312', '6313', '6314', '6315', '6316', '6321', '6322', '6331', '6332', '6341', '6342', '6343', '6344', '6345', '6346', '6411', '6421', '6511', '6512', '6513', '6521', '6522', '6523', '6524', '6525', '6531', '6532', '6533', '6541', '6551', '6552', '6561', '6562', '6563', '6564', '6611', '6621', '6622', '6623', '6711', '6721', '6722', '6731', '6732', '6733', '6741', '6742', '7201', '7202', '7203', '7204', '7205', '7231', '7232', '7233', '7234', '7235', '7236', '7237', '7241', '7242', '7243', '7244', '7245', '7246', '7247', '7251', '7252', '7253', '7271', '7272', '7281', '7282', '7283', '7284', '7291', '7292', '7293', '7294', '7295', '7301', '7302', '7303', '7304', '7305', '7311', '7312', '7313', '7314', '7315', '7316', '7318', '7321', '7322', '7331', '7332', '7333', '7334', '7335', '7361', '7362', '7371', '7372', '7373', '7381', '7384', '7441', '7442', '7444', '7445', '7451', '7452', '7511', '7512', '7513', '7514', '7521', '7522', '7531', '7532', '7533', '7534', '7535', '7611', '7612', '7621', '7622', '8211', '8221', '8222', '8231', '8232', '8241', '8252', '8255', '8261', '8262', '8411', '8412', '8421', '8422', '8431', '8432', '8441', '8442', '8611', '8612', '8613', '8614', '8615', '8616', '9211', '9212', '9213', '9214', '9215', '9217', '9221', '9222', '9223', '9224', '9226', '9227', '9231', '9232', '9235', '9241', '9243', '9411', '9412', '9413', '9414', '9415', '9416', '9417', '9418', '9421', '9422', '9423', '9431', '9432', '9433', '9434', '9435', '9436', '9437', '9441', '9442', '9445', '9446', '9447', '9461', '9462', '9463', '9465', '9471', '9472', '9473', '9474', '9521', '9522', '9523', '9524', '9525', '9526', '9527', '9531', '9532', '9533', '9534', '9535', '9536', '9537', '9611', '9612', '9613', '9614', '9615', '9616', '9617', '9618', '9619']



base_url="https://jackyzhang.pro/"
# base_url="http://127.0.0.1:8000/"
api_url={
    'noclist':"noc/api/noclist/",
    "programlist":"noc/programlist/",
    "wage":"noc/wage/",
    "outlook":"noc/outlook/",
    "preferrednocs":'noc/preferrednocs/',
    "preferredareas":'noc/preferredareas',
    "nocinfo":"noc/api/nocs"
}
param_data="0114/77"

# kw, main_duties,title_examples
# noc
# noc/area
# starts_with,area,outlook
# noc, outlook
# noc



def getData(api_url_key,param_data=None):
    url=base_url+api_url.get(api_url_key,'')
    response=requests.get(url,params=param_data,headers={'Authorization': "Token c575ff86cdd0385dd504960db9475ba0bcd3da45"})  
    if response.status_code==200:
        return response.json()
    else:
        return []

def getNocCodes(args):
    d=enchant.Dict("en_US")
    error=None
    keywords=args.keywords
    for kw in keywords:
        if d.check(kw)==False:
            print(colored(kw,"red")," spelled error. Suggestion: ",colored(" ,".join(d.suggest(kw)),"green"))
            error=True
    if error:
        exit(0)
    else:
        param_data={'kw':' '.join(keywords)}
        if args.main_duties:
            param_data={**param_data,**{"main_duties":True}}
        if args.title_examples:
            param_data={**param_data,**{"title_examples":True}}
        result=getData("noclist",param_data)
        utils.printListDict(result)
        return 0

def getPrograms(args):
    param_data={'noc':args.noc}
    result=getData("programlist",param_data)
    utils.printListDict(result)
    return 0

def getWageOutlook(args):
    noc=args.noc or '1111'
    area=int(args.area or 77)
    param_data={
        'noc':noc,
        'area':area
    }
    result={**getData('wage',param_data),**getData('outlook',param_data)}
    outpout=[
        ['Province','Area','NOC','Outlook','Lowest','Median','Highest'],
        [utils.area_info[area][0],utils.area_info[area][1],result.get('noc'),result.get('outlook','N/A'),result.get('lowest','N/A'),result.get('median','N/A'),result.get('highest','N/A')]
        ]
    
    utils.printFList2D(outpout)

    return result

def getPreferredNocs(args):
    area=int(args.area or 77)
    param_data={
        "starts_with":args.starts_with or '',
        "area":area,
        "outlook":args.outlook or 3
    }
    
    result=getData('preferrednocs',param_data)
    if len(result)>0:
        print(f'Qualified nocs in area {utils.area_info[area][1]},{utils.area_info[area][0]} are: ')
        utils.printListDict(result)
        return result
    else:
        print(colored('no mactching records... ','red'))
        return 0

def getPreferredAreas(args):
    noc=args.noc or '1111'
    outlook=args.outlook or 3
    param_data={
        "noc":noc,
        "outlook":outlook
    }
    result=getData('preferredareas',param_data)
    if len(result)>0:
        print(f'Qualified areas are: ')
        utils.printListDict(result)
        return result
    else:
        print(colored('no mactching records... ','red'))
        return 0

def getDetails(args):
    noc=args.noc or '1111'
    url=base_url+api_url['nocinfo']+'/'+str(noc)+'/'
    result=requests.get(url,headers={'Authorization': "Token c575ff86cdd0385dd504960db9475ba0bcd3da45"}).json()

    detail=args.detail
    if detail=='tt':
        print(colored(f'\nTitle of noc {noc}:\n','green'))
        print(result['title'])
        return 
    if detail=='te':
        print(colored(f'\nTitle examples of noc {noc}:\n','green'))
        print(result['title_examples'])
        return 
    elif detail=='md':
        print(colored(f'\nMain duties of noc {noc}:\n','green'))
        print(result['main_duties'])
        return 
    elif detail=='gd':
        print(colored(f'\nGeneral description of noc {noc}:\n','green'))
        print(result['general_description'])
        return 
    elif detail=='er':
        print(colored(f'\nEmployment requirements of noc {noc}:\n','green'))
        print(result['employment_requirements'])
        return 
    elif detail=='ai':
        print(colored(f'\nAdditional information of noc {noc}:\n','green'))
        print(result['additional_information'])
        return 
    elif detail=='ex':
        print(colored(f'\nExcluded titles of noc {noc}:\n','green'))
        print(result['exclusion'])
        return 
    else:    
        print(colored(f'\nAll information of noc {noc}:\n','green'))
        for k,v in result.items():
            k=k.replace('_',' ').title()
            print(colored(f'{k}:','green'))
            print(v,'\n')
    return result

def main():
    parser=argparse.ArgumentParser(description="used for processing everything noc related")
    parser.add_argument("-n", "--noc", help="input noc code")
    
    # Get noc codes by searching keywords
    parser.add_argument("-k", "--keywords", help="input key words",nargs='+')
    parser.add_argument("-md","--main_duties",help="input if includes main duties",action="store_true")
    parser.add_argument("-te","--title_examples",help="input if includes title examples",action="store_true")

    # Get specific noc related programs 
    parser.add_argument("-p", "--program", help="list spcial programs",action="store_true")

    # Get Wage and Outlook 
    parser.add_argument("-w", "--wage", help="get wage and outlook info",action="store_true")
    parser.add_argument("-a","--area",help="input area index")
    
    # parser.add_argument("-f", "--final", help="get final wage and outlook info",action="store_true")
    parser.add_argument("-s", "--starts_with", help="noc starts with")
    # parser.add_argument("-l", "--list", help="list noc begins with xxx",action="store_true")
    parser.add_argument("-o", "--outlook", help="input outlook star number",type=int,choices=range(1,4))

    # Preferred areas
    # for both -n & -o 

    # parser.add_argument("-mw", "--medianwages", help="list all province median wages",action="store_true")
    # parser.add_argument("-tw", "--top10wages", help="list all province top 10 wages",action="store_true")
    # parser.add_argument("-pd", "--program_details", help="input key words in a program",nargs='+')
    parser.add_argument("-i", "--information", help="list area indeices",action="store_true")
    
    # Get noc all information
    parser.add_argument("-d","--detail",help=" for display a noc information. md: main duties, tt: title,te: title examples,gd: general description,er: employment requirements,ai: additional information,ec: exclusion,all: for all information ")
    # parser.add_argument("-rm", "--remote", help="Get information from websites",action="store_true") # TODO: 需要保留，可以把原来的做到库里面。

    args = parser.parse_args()

    if args.information:
        utils.printFList2D(utils.area_info)
        return 0 
    if args.noc:
        if args.noc not in noc_list:
            print(colored("noc code invalid...",'red'))
            return 0

    if args.keywords:
        getNocCodes(args)    
        return 0
    
    if args.program:
        getPrograms(args)
        return 0

    if args.wage :
        getWageOutlook(args)
        return 0
    
    if args.starts_with:
        getPreferredNocs(args)
        return 0
    
    if bool(args.noc) & bool(args.outlook):
        getPreferredAreas(args)
        return 0
    
    if args.detail:
        getDetails(args)
        return 0

    
    
if __name__=="__main__":
    main()
