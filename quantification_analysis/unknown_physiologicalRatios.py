
class physiological_ratios():
    def __init__(self):
        self.ratios = {'accoa_ratio':{'component_group_name':["accoa","coa"],'name':'Ac(CoA) Ratio','description':'accoa/(coa+accoa)'},
                    'ec':{'component_group_name':["adp","amp","atp"],'name':'Adenylate charge','description':'(0.5*adp+atp)/(adp+amp+atp)'},
                    'p_ratio01':{'component_group_name':["adp","atp"],'name':'Adenylate ratio01','description':'atp/adp'},
                    'p_ratio02':{'component_group_name':["amp","atp"],'name':'Adenylate ratio02','description':'atp/amp'},
                    'redox_ratio':{'component_group_name':["gthox","gthrd"],'name':'Redox ratio','description':'gthrd/(gthox+gthrd)'},
                    'gth_ratio01':{'component_group_name':["gthox","gthrd"],'name':'Glutathione ratio01','description':'gthrd/gthox'},
                    'mar_ak':{'component_group_name':["adp","amp","atp"],'name':'Mass action ratio of the adenylate kinase reaction','description':'(amp*atp)/(adp*adp)'},
                    'mar_fum':{'component_group_name':["fum","mal-L"],'name':'Mass action of the fumarase reaction','description':'fum/mal-L'},
                    'mar_pgi':{'component_group_name':["f6p","g6p"],'name':'Mass action ratio of the PGI reaction','description':'f6p/g6p'},
                    'mar_pgm_eno':{'component_group_name':["Pool_2pg_3pg","pep"],'name':'Mass action ratio of the PGM and ENO reactions','description':'pep/Pool_2pg_3pg'},
                    #'n2_ratio01':{'component_group_name':["gln-L","glu-L"],'name':'Nitrogen ratio01','description':'gln-L/(gln-L+glu-L)'},
                    'n2_ratio01':{'component_group_name':["gln-L","glu-L"],'name':'Nitrogen ratio01','description':'gln-L/glu-L'},
                    #'n2_ratio02':{'component_group_name':["akg","glu-L"],'name':'Nitrogen ratio02','description':'glu-L/(akg+glu-L)'},
                    'n2_ratio02':{'component_group_name':["akg","glu-L"],'name':'Nitrogen ratio02','description':'glu-L/akg'},
                    'n2_ratio03':{'component_group_name':["akg","gln-L"],'name':'Nitrogen ratio03','description':'gln-L/akg'},
                    'nc':{'component_group_name':["akg","gln-L","glu-L"],'name':'Nitrogen charge','description':'(0.5*glu-L+gln-L)/(akg+glu-L+gln-L)'},
                    'nad_ratio':{'component_group_name':["nad","nadh"],'name':'NAD(H) ratio','description':'nadh/(nad+nadh)'},
                    'nadp_ratio':{'component_group_name':["nadp","nadph"],'name':'NADP(H) ratio','description':'nadph/(nadp+nadph)'},
                    'nad(p)_ratio':{'component_group_name':["nadp","nadph","nad","nadh"],'name':'NAD(P)(H) ratio','description':'(nadph+nadh)/(nadp+nadph+nad+nadh)'}};

    def calculate_physiologicalRatios(self,ratio_id_I,ratio_mets_I):
        '''Calculate physiological ratios
        Input:
         ratio_id_I = string
         ratio_mets_I = {component_group_name:float}
        Output:
         'ratio_O':float
         'num_O':float
         'den_O':float
        '''
        
        ratio_O = None;
        num_O = None;
        den_O = None
        if ratio_id_I == 'accoa_ratio':
            num_O = ratio_mets_I["accoa"]
            den_O = ratio_mets_I["coa"]+ratio_mets_I["accoa"]
            ratio_O = ratio_mets_I["accoa"]/(ratio_mets_I["coa"]+ratio_mets_I["accoa"])
        elif ratio_id_I == 'ec':
            num_O = 0.5*ratio_mets_I["adp"]+ratio_mets_I["atp"]
            den_O = ratio_mets_I["adp"]+ratio_mets_I["amp"]+ratio_mets_I["atp"]
            ratio_O = (0.5*ratio_mets_I["adp"]+ratio_mets_I["atp"])/(ratio_mets_I["adp"]+ratio_mets_I["amp"]+ratio_mets_I["atp"])
        elif ratio_id_I == 'p_ratio01':
            num_O = ratio_mets_I["atp"]
            den_O = ratio_mets_I["adp"]
            ratio_O = ratio_mets_I["atp"]/ratio_mets_I["adp"]
        elif ratio_id_I == 'p_ratio02':
            num_O = ratio_mets_I["atp"]
            den_O = ratio_mets_I["amp"]
            ratio_O = ratio_mets_I["atp"]/ratio_mets_I["amp"]
        elif ratio_id_I == 'redox_ratio':
            num_O = ratio_mets_I["gthrd"]
            den_O = ratio_mets_I["gthox"]+ratio_mets_I["gthrd"]
            ratio_O = ratio_mets_I["gthrd"]/(ratio_mets_I["gthox"]+ratio_mets_I["gthrd"])
        elif ratio_id_I == 'gth_ratio01':
            num_O = ratio_mets_I["gthrd"]
            den_O = ratio_mets_I["gthox"]
            ratio_O = ratio_mets_I["gthrd"]/ratio_mets_I["gthox"]
        elif ratio_id_I == 'mar_ak':
            num_O = ratio_mets_I["amp"]*ratio_mets_I["atp"]
            den_O = ratio_mets_I["adp"]*ratio_mets_I["adp"]
            ratio_O = (ratio_mets_I["amp"]*ratio_mets_I["atp"])/(ratio_mets_I["adp"]*ratio_mets_I["adp"])
        elif ratio_id_I == 'mar_fum':
            num_O = ratio_mets_I["fum"]
            den_O = ratio_mets_I["mal-L"]
            ratio_O = ratio_mets_I["fum"]/ratio_mets_I["mal-L"]
        elif ratio_id_I == 'mar_pgi':
            num_O = ratio_mets_I["f6p"]/ratio_mets_I["g6p"]
            den_O = ratio_mets_I["f6p"]/ratio_mets_I["g6p"]
            ratio_O = ratio_mets_I["f6p"]/ratio_mets_I["g6p"]
        elif ratio_id_I == 'mar_pgm_eno':
            num_O = ratio_mets_I["pep"]
            den_O = ratio_mets_I["Pool_2pg_3pg"]
            ratio_O = ratio_mets_I["pep"]/ratio_mets_I["Pool_2pg_3pg"]
        #elif ratio_id_I == 'n2_ratio01':
        #    ratio_O = ratio_mets_I["gln-L"]/(ratio_mets_I["gln-L"]+ratio_mets_I["glu-L"])
        #elif ratio_id_I == 'n2_ratio02':
        #    ratio_O = ratio_mets_I["glu-L"]/(ratio_mets_I["akg"]+ratio_mets_I["glu-L"])
        elif ratio_id_I == 'n2_ratio01':
            num_O = ratio_mets_I["gln-L"]
            den_O = ratio_mets_I["glu-L"]
            ratio_O = ratio_mets_I["gln-L"]/ratio_mets_I["glu-L"]
        elif ratio_id_I == 'n2_ratio02':
            num_O = ratio_mets_I["glu-L"]
            den_O = ratio_mets_I["akg"]
            ratio_O = ratio_mets_I["glu-L"]/ratio_mets_I["akg"]
        elif ratio_id_I == 'n2_ratio03':
            num_O = ratio_mets_I["gln-L"]
            den_O = ratio_mets_I["akg"]
            ratio_O = ratio_mets_I["gln-L"]/ratio_mets_I["akg"]
        elif ratio_id_I == 'nc':
            num_O = 0.5*ratio_mets_I["glu-L"]+ratio_mets_I["gln-L"]
            den_O = ratio_mets_I["akg"]+ratio_mets_I["glu-L"]+ratio_mets_I["gln-L"]
            ratio_O = (0.5*ratio_mets_I["glu-L"]+ratio_mets_I["gln-L"])/(ratio_mets_I["akg"]+ratio_mets_I["glu-L"]+ratio_mets_I["gln-L"])
        elif ratio_id_I == 'nad_ratio':
            num_O = ratio_mets_I["nadh"]
            den_O = ratio_mets_I["nad"]+ratio_mets_I["nadh"]
            ratio_O = ratio_mets_I["nadh"]/(ratio_mets_I["nad"]+ratio_mets_I["nadh"])
        elif ratio_id_I == 'nadp_ratio':
            num_O = ratio_mets_I["nadph"]
            den_O = ratio_mets_I["nadp"]+ratio_mets_I["nadph"]
            ratio_O = ratio_mets_I["nadph"]/(ratio_mets_I["nadp"]+ratio_mets_I["nadph"])
        elif ratio_id_I == 'nad(p)_ratio':
            num_O = ratio_mets_I["nadph"]+ratio_mets_I["nadh"]
            den_O = ratio_mets_I["nadp"]+ratio_mets_I["nadph"]+ratio_mets_I["nad"]+ratio_mets_I["nadh"]
            ratio_O = (ratio_mets_I["nadph"]+ratio_mets_I["nadh"])/(ratio_mets_I["nadp"]+ratio_mets_I["nadph"]+ratio_mets_I["nad"]+ratio_mets_I["nadh"])
        else:
            print('ratio_id not recognized')
        return ratio_O,num_O,den_O;