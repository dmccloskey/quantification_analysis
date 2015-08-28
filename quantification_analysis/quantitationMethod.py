from copy import copy
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from calculate_utilities.r import robjects,importr

class quantitationMethod():
    def __init__(self,id_I=[], q1_mass_I=[],q3_mass_I=[], met_id_I=[],component_name_I=[],is_name_I=[],fit_I=[],
                 weighting_I=[],intercept_I=[],slope_I=[],correlation_I=[],use_area_I=[],lloq_I=[],uloq_I=[],
                 points_I=[]):
        self.qmethod = [];

    def _set_qmethod(self,
                 id_I=[], q1_mass_I=[],q3_mass_I=[], met_id_I=[],component_name_I=[],is_name_I=[],fit_I=[],
                 weighting_I=[],intercept_I=[],slope_I=[],correlation_I=[],use_area_I=[],lloq_I=[],uloq_I=[],
                 points_I=[]):
        '''make rows of a quantitation method table'''
        qmethod_O = [];
        qmrow = quantitation_method_row();
        for cnt,c in enumerate(component_name_I):
            qmrow._set_qmethod_row(id_I[cnt], q1_mass_I[cnt],q3_mass_I[cnt], met_id_I[cnt],component_name_I[cnt],is_name_I[cnt]);
            qmethod_O.append(copy(qmrow.qmethod_row));
            qmrow.clear_data();
        self.qmethod = qmethod_O;

    def make_qmethod(self,
                 id_I=[], q1_mass_I=[],q3_mass_I=[], met_id_I=[],component_name_I=[],is_name_I=[],
                 fit_I=[],weighting_I=[],use_area_I=[],
                 actual_concentration_I=[[]],area_ratio_I=[[]],
                 height_ratio_I=[[]],dilution_factor_I=[[]]):
        '''make rows of a quantitation method table'''
        qmethod_O = [];
        qmrow = quantitation_method_row();
        for cnt,c in enumerate(component_name_I):
            qmrow._set_qmethod_row(id_I[cnt], q1_mass_I[cnt],q3_mass_I[cnt], met_id_I[cnt],component_name_I[cnt],is_name_I[cnt]);
            qmrow.calculate_regressionParameters(fit_I[cnt], weighting_I[cnt], use_area_I[cnt],
                                       actual_concentration_I[cnt],area_ratio_I[cnt],height_ratio_I[cnt],dilution_factor_I[cnt])
            qmethod_O.append(copy(qmrow.qmethod_row));
            qmrow.clear_data();  
        self.qmethod = qmethod_O;

    def export_qmethod_js(self,data_dir = 'tmp'):
        '''export the qmethods for visualization using ddt'''
        return

    def import_qmethod(self,QMethod_id_I,filename_I):
        """import qmethod"""
        io = base_importData();
        io.read_csv(filename_I);
        self.qmethod = self._set_qmethod_multiQuant(QMethod_id_I,io.data);

    def _set_qmethod_multiQuant(self,QMethod_id_I,data_I):
        """set the qmethod from a list of dictionaries"""
        qmethod_O = [];
        qmrow = quantitation_method_row();
        self.qmethod = qmethod_O;
        for d in data_I:
            qmrow._set_qmethod_row(QMethod_id_I,
                        d['Q1 Mass - 1'],
                        d['Q3 Mass - 1'],
                        d['Group Name'],
                        d['Name'],
                        d['IS Name'],
                        d['Regression Type'],
                        d['Regression Weighting'],
                        None,
                        None,
                        None,
                        d['Use Area'],
                        None,
                        None,
                        None);
            qmethod_O.append(copy(qmrow.qmethod_row));
            qmrow.clear_data();
        return qmethod_O;

    def _parse_calibrators(self,use_area_I,actual_concentration_I,area_ratio_I,height_ratio_I,dilution_factor_I):
        '''make the calibrator structure
        INPUT:
            use_area_I = boolean, use the area for quantification if true, use the peak height for quantification if false
            actual_concentration_I = float array, actual concentration of each sample
            area_ratio_I = float array, area ratio of the analyte to IS
            height_ratio_I = float array, peak height ratio of the analyte to IS
            dilution_factor_I = float array, dilution factor of the sample (e.g., 1, 10, etc.)'''

        # check input
        if len(actual_concentration_I) != len(area_ratio_I) or len(actual_concentration_I) != len(height_ratio_I) or len(actual_concentration_I) != len(dilution_factor_I):
            print('the number of the actual_concentrations does not match the number of area_ratios, height_ratios, or dilution_factors');
            exit(-1);

        # variable to check quantitation
        calc_regress = True;

        ## parse input:
        #calibrators_O = [];
        #for cnt,c in actual_concentration_I:
        #    calibrators.append({'actual_concentration':actual_concentration_I,
        #                'area_ratio':area_ratio_I,
        #                'height_ratio':height_ratio_I,
        #                'dilution_factor':dilution_factor_I});

        # extraction concentrations
        concentration = [];
        for c in actual_concentration_I: 
            if c: concentration.append(c);
            else: calc_regress = False;
        if len(concentration)==0:
            calc_regress = False;
        # extraction ratio
        ratio = [];
        if use_area_I:
            for c in area_ratio_I: 
                if c: ratio.append(c);
                else: ratio.append(0.0);
        else:
            for c in height_ratio_I:
                if c: ratio.append(c);
                else: ratio.append(0.0);
        if len(ratio)==0:
            calc_regress = False;
        # extraction diluton factor
        dilution_factor = [];
        for c in dilution_factor_I:
            if c: dilution_factor.append(c);
            else: dilution_factor.append(1.0);
        # correct the concentration for the dilution factor
        for n in range(len(concentration)):
            concentration[n] = concentration[n]/dilution_factor[n];

        return calc_regress, concentration, ratio;


    def calculate_regressionParameters(self, fit_I, weighting_I, use_area_I,
                                       actual_concentration_I,area_ratio_I,height_ratio_I,dilution_factor_I):
        '''calculate regression parameters for a given component
        from a specified quantitation method id
        NOTE: intended to be used in a loop
        input:
            sample_names_I = string array, samples that were used to generate the calibration curve
            component_name_I = string, component_name
            fit_I = string, type of fit
            weighting_I = string, type of weighting
            use_area_I = boolean, use the area for quantification if true, use the peak height for quantification if false
            actual_concentration_I = float array, actual concentration of each sample
            area_ratio_I = float array, area ratio of the analyte to IS
            height_ratio_I = float array, peak height ratio of the analyte to IS
            dilution_factor_I = float array, dilution factor of the sample (e.g., 1, 10, etc.);
        ouput:
            slope
            intercept
            correlation
            lloq
            uloq
            points'''
        
        calc_regress, concentration, ratio = self._parse_calibrators(use_area_I,
                                       actual_concentration_I,area_ratio_I,height_ratio_I,dilution_factor_I);

        
        self.qmethod['fit'] = fit_I;
        self.qmethod_row['weighting'] = weighting_I;
        self.qmethod_row['intercept'] = 0.0;
        self.qmethod_row['slope'] = 0.0;
        self.qmethod_row['correlation'] = 0.0;
        self.qmethod_row['use_area'] = use_area_I;
        self.qmethod_row['lloq'] = 0.0;
        self.qmethod_row['uloq'] = 0.0;
        self.qmethod_row['points'] = 0;

        if (not(calc_regress)):
            print('bad regression data: regression not performed');
            return;
            #return 0,0,0,0,0,0;

        # lloq, uloq, points
        lloq_O = min(concentration);
        uloq_O = max(concentration);
        points_O = len(concentration);

        # Call to R
        try:
            stats = importr('stats');

            # generate weights:
            '''From MultiQuant Manual:
            Weighting type	Weight (w)
            None Always	1.0.
            1 / x	If |x| < 10-5 then w = 10e5; otherwise w = 1 / |x|.
            1 / x2	If |x| < 10-5 then w = 10e10; otherwise w = 1 / x2.
            1 / y	If |y| < 10-8 then w = 10e8; otherwise w = 1 / |y|.
            1 / y2	If |y| < 10-8 then w = 10e16; otherwise w = 1 / y2.
            ln x	If x < 0 an error is generated; otherwise if x < 10-5 then w = ln 105,
		            otherwise w = |ln x|.'''
            wts = []; 
            if weighting_I == 'ln (x)':
                for c in concentration:
                    if c<10e-5:
                        wts.append(log(10e5));
                    else:
                        wts.append(abs(log(c)));
            elif weighting_I == 'None':
                for c in concentration:
                    wts.append(1.0);
            elif weighting_I == '1 / x':
                for c in concentration:
                    if c<10e-5:
                        wts.append(1/10e5);
                    else:
                        wts.append(1/abs(c));
            elif weighting_I == '1 / y':
                for c in ratio:
                    if c<10e-8:
                        wts.append(1/10e8);
                    else:
                        wts.append(1/abs(c));

            else:
                print(("weighting " + weighting_I + " not yet supported"));
                print("linear weighting used instead");
                for c in concentration:
                    wts.append(1.0);
            
            # convert lists to R objects
            x = robjects.FloatVector(concentration);
            y = robjects.FloatVector(ratio);
            w = robjects.FloatVector(wts);
            if fit_I == 'Linear':
                fmla = robjects.Formula('y ~ x'); # generate the R formula for lm
            elif fit_I == 'Linear Through Zero':
                fmla = robjects.Formula('y ~ -1 + x'); # generate the R formula for lm
            elif fit_I == 'Quadratic':
                fmla = robjects.Formula('y ~ x + I(x^2)'); # generate the R formula for lm
            elif fit_I == 'Power':
                fmla = robjects.Formula('log(y) ~ log(x)'); # generate the R formula for lm
            else:
                print(("fit " + fit_I + " not yet supported"));
                print("linear model used instead");
                fmla = robjects.Formula('y ~ x');

            env = fmla.environment; # set the local environmental variables for lm
            env['x'] = x;
            env['y'] = y;
            #fit = r('lm(%s)' %fmla.r_repr()); # direct call to R
            fit = stats.lm(fmla, weights = w); # return the lm fitted model from R
            sum = stats.summary_lm(fit) # return the summary of the fit
            intercept_O = sum.rx2('coefficients')[0]; #intercept
            slope_O = sum.rx2('coefficients')[1]; #slope
            correlation_O = sum.rx2('r.squared')[0]; #r-squared

            
            self.qmethod_row['intercept'] = intercept_O;
            self.qmethod_row['slope'] = slope_O;
            self.qmethod_row['correlation'] = correlation_O;
            self.qmethod_row['lloq'] = lloq_O;
            self.qmethod_row['uloq'] = uloq_O;
            self.qmethod_row['points'] = points_O;
            #return slope_O, intercept_O, correlation_O, lloq_O, uloq_O, points_O;
        except:
            print('error in R')

class quantitationMethod_row():
    def __init__(self,id_I=None, q1_mass_I=None,q3_mass_I=None, met_id_I=None,component_name_I=None,is_name_I=None):
        self.qmethod_row = self._set_qmethod_row(id_I, q1_mass_I,q3_mass_I, met_id_I,component_name_I,is_name_I);

    def _set_qmethod_row(self, id_I=None, q1_mass_I=None,q3_mass_I=None, met_id_I=None,component_name_I=None,is_name_I=None,fit_I=None,
                 weighting_I=None,intercept_I=None,slope_I=None,correlation_I=None,use_area_I=None,lloq_I=None,uloq_I=None,
                 points_I=None):
        '''make a row of a quantitation method table'''
        qmethod_row = {};
        qmethod_row['id'] = id_I;
        qmethod_row['q1_mass'] = q1_mass_I;
        qmethod_row['q3_mass'] = q3_mass_I;
        qmethod_row['met_id'] = met_id_I;
        qmethod_row['component_name'] = component_name_I;
        qmethod_row['is_name'] = is_name_I;
        qmethod_row['fit'] = fit_I;
        qmethod_row['weighting'] = weighting_I;
        qmethod_row['intercept'] = intercept_I;
        qmethod_row['slope'] = slope_I;
        qmethod_row['correlation'] = correlation_I;
        qmethod_row['use_area'] = use_area_I;
        qmethod_row['lloq'] = lloq_I;
        qmethod_row['uloq'] = uloq_I;
        qmethod_row['points'] = points_I;
        return qmethod_row;

    def clear_data(self):
        self.qmethod_row = {};