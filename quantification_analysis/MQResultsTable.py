from copy import copy
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData

class MQResultsTable():
    def __init__(self):
        self.resultsTable = [];

    def clear_data(self):
        del self.resultsTable[:];

    def _set_resultTable_multiQuant(self,data_I):
        """set the results table from a list of dictionaries"""
        resultsTable = [];
        rtrow = MQResultsTable_row();
        for d in data_I:
            tmp = {};
            tmp = rtrow._set_resultsTable_row(d['Index'],
                            d['Sample Index'],
                            d['Original Filename'],
                            d['Sample Name'],
                            d['Sample ID'],
                            d['Sample Comment'],
                            d['Sample Type'],
                            d['Acquisition Date & Time'],
                            d['Rack Number'],
                            d['Plate Number'],
                            d['Vial Number'],
                            d['Dilution Factor'],
                            d['Injection Volume'],
                            d['Operator Name'],
                            d['Acq. Method Name'],
                            d['IS'],
                            d['Component Name'],
                            d['Component Index'],
                            d['Component Comment'],
                            d['IS Comment'],
                            d['Mass Info'],
                            d['IS Mass Info'],
                            d['IS Name'],
                            d['Component Group Name'],
                            d['Conc. Units'],
                            d['Failed Query'],
                            d['IS Failed Query'],
                            d['Peak Comment'],
                            d['IS Peak Comment'],
                            d['Actual Concentration'],
                            d['IS Actual Concentration'],
                            d['Concentration Ratio'],
                            d['Expected RT'],
                            d['IS Expected RT'],
                            d['Integration Type'],
                            d['IS Integration Type'],
                            d['Area'],
                            d['IS Area'],
                            d['Corrected Area'],
                            d['IS Corrected Area'],
                            d['Area Ratio'],
                            d['Height'],
                            d['IS Height'],
                            d['Corrected Height'],
                            d['IS Corrected Height'],
                            d['Height Ratio'],
                            d['Area / Height'],
                            d['IS Area / Height'],
                            d['Corrected Area/Height'],
                            d['IS Corrected Area/Height'],
                            d['Region Height'],
                            d['IS Region Height'],
                            d['Quality'],
                            d['IS Quality'],
                            d['Retention Time'],
                            d['IS Retention Time'],
                            d['Start Time'],
                            d['IS Start Time'],
                            d['End Time'],
                            d['IS End Time'],
                            d['Total Width'],
                            d['IS Total Width'],
                            d['Width at 50%'],
                            d['IS Width at 50%'],
                            d['Signal / Noise'],
                            d['IS Signal / Noise'],
                            d['Baseline Delta / Height'],
                            d['IS Baseline Delta / Height'],
                            d['Modified'],
                            d['Relative RT'],
                            d['Used'],
                            d['Calculated Concentration'],
                            d['Accuracy'],
                            d['Comment'],
                            d['Use_Calculated_Concentration']);
            resultsTable.append(tmp);

        return resultsTable;

    def import_resultsTable(self,filename_I):
        """import resultsTable"""
        io = base_importData();
        io.read_csv(filename_I);
        self.resultsTable = self._set_resultTable_multiQuant(io.data);

    def export_resultsTable(self,filename_O):
        """export resultsTable"""
        io = base_exportData(self.resultsTable);
        io.write_dict2csv(filename_O);

class MQResultsTable_row():
    def __init__(self):
        self.resultsTable_row = {};

    def clear_data(self):
        self.resultsTable_row = {};

    def format_data(self,data_I):
        """remove specific sequences for utf-8 compatibility"""
        row = {};
        if data_I:
            try:
                for key, value in data_I.items():
                    # replace multiquant-specific output
                    if (value == 'N/A' or value == '< 0' or value == '<2 points' or
                        value == 'degenerate' or value == '(No IS)'): value = None;
                    # replace empty strings with None
                    if not(value):
                        value = None;
                    else:
                        #value.decode('utf-8', "ignore"); # convert to utf-8      
                        value = value;           
                    row[key] = value;
            except BaseException as e:
                sys.exit('error formating data %s' % d);  
        return row;

    def _set_resultsTable_row(self,
                 index__I=None,sample_index_I=None,original_filename_I=None,
                 sample_name_I=None,sample_id_I=None,sample_comment_I=None,sample_type_I=None,
                 acquisition_date_and_time_I=None,rack_number_I=None,plate_number_I=None,
                 vial_number_I=None,dilution_factor_I=None,injection_volume_I=None,
                 operator_name_I=None,acq_method_name_I=None,is__I=None,component_name_I=None,
                 component_index_I=None,component_comment_I=None,is_comment_I=None,
                 mass_info_I=None,is_mass_I=None,is_name_I=None,component_group_name_I=None,
                 conc_units_I=None,failed_query_I=None,is_failed_query_I=None,peak_comment_I=None,
                 is_peak_comment_I=None,actual_concentration_I=None,is_actual_concentration_I=None,
                 concentration_ratio_I=None,expected_rt_I=None,is_expected_rt_I=None,
                 integration_type_I=None,is_integration_type_I=None,area_I=None,is_area_I=None,
                 corrected_area_I=None,is_corrected_area_I=None,area_ratio_I=None,height_I=None,
                 is_height_I=None,corrected_height_I=None,is_corrected_height_I=None,
                 height_ratio_I=None,area_2_height_I=None,is_area_2_height_I=None,
                 corrected_area2height_I=None,is_corrected_area2height_I=None,
                 region_height_I=None,is_region_height_I=None,quality_I=None,is_quality_I=None,
                 retention_time_I=None,is_retention_time_I=None,start_time_I=None,
                 is_start_time_I=None,end_time_I=None,is_end_time_I=None,total_width_I=None,
                 is_total_width_I=None,width_at_50_I=None,is_width_at_50_I=None,
                 signal_2_noise_I=None,is_signal_2_noise_I=None,baseline_delta_2_height_I=None,
                 is_baseline_delta_2_height_I=None,modified__I=None,relative_rt_I=None,used__I=None,
                 calculated_concentration_I=None,accuracy__I=None,comment__I=None,use_calculated_concentration_I=None):
        resultsTable_row = {};
        resultsTable_row['index_']=index__I;
        resultsTable_row['sample_index']=sample_index_I;
        resultsTable_row['original_filename']=original_filename_I;
        resultsTable_row['sample_name']=sample_name_I;
        resultsTable_row['sample_id']=sample_id_I;
        resultsTable_row['sample_comment']=sample_comment_I;
        resultsTable_row['sample_type']=sample_type_I;
        resultsTable_row['acquisition_date_and_time']=acquisition_date_and_time_I;
        resultsTable_row['rack_number']=rack_number_I;
        resultsTable_row['plate_number']=plate_number_I;
        resultsTable_row['vial_number']=vial_number_I;
        resultsTable_row['dilution_factor']=dilution_factor_I;
        resultsTable_row['injection_volume']=injection_volume_I;
        resultsTable_row['operator_name']=operator_name_I;
        resultsTable_row['acq_method_name']=acq_method_name_I;
        resultsTable_row['is_']=is__I;
        resultsTable_row['component_name']=component_name_I;
        resultsTable_row['component_index']=component_index_I;
        resultsTable_row['component_comment']=component_comment_I;
        resultsTable_row['is_comment']=is_comment_I;
        resultsTable_row['mass_info']=mass_info_I;
        resultsTable_row['is_mass']=is_mass_I;
        resultsTable_row['is_name']=is_name_I;
        resultsTable_row['component_group_name']=component_group_name_I;
        resultsTable_row['conc_units']=conc_units_I;
        resultsTable_row['failed_query']=failed_query_I;
        resultsTable_row['is_failed_query']=is_failed_query_I;
        resultsTable_row['peak_comment']=peak_comment_I;
        resultsTable_row['is_peak_comment']=is_peak_comment_I;
        resultsTable_row['actual_concentration']=actual_concentration_I;
        resultsTable_row['is_actual_concentration']=is_actual_concentration_I;
        resultsTable_row['concentration_ratio']=concentration_ratio_I;
        resultsTable_row['expected_rt']=expected_rt_I;
        resultsTable_row['is_expected_rt']=is_expected_rt_I;
        resultsTable_row['integration_type']=integration_type_I;
        resultsTable_row['is_integration_type']=is_integration_type_I;
        resultsTable_row['area']=area_I;
        resultsTable_row['is_area']=is_area_I;
        resultsTable_row['corrected_area']=corrected_area_I;
        resultsTable_row['is_corrected_area']=is_corrected_area_I;
        resultsTable_row['area_ratio']=area_ratio_I;
        resultsTable_row['height']=height_I;
        resultsTable_row['is_height']=is_height_I;
        resultsTable_row['corrected_height']=corrected_height_I;
        resultsTable_row['is_corrected_height']=is_corrected_height_I;
        resultsTable_row['height_ratio']=height_ratio_I;
        resultsTable_row['area_2_height']=area_2_height_I;
        resultsTable_row['is_area_2_height']=is_area_2_height_I;
        resultsTable_row['corrected_area2height']=corrected_area2height_I;
        resultsTable_row['is_corrected_area2height']=is_corrected_area2height_I;
        resultsTable_row['region_height']=region_height_I;
        resultsTable_row['is_region_height']=is_region_height_I;
        resultsTable_row['quality']=quality_I;
        resultsTable_row['is_quality']=is_quality_I;
        resultsTable_row['retention_time']=retention_time_I;
        resultsTable_row['is_retention_time']=is_retention_time_I;
        resultsTable_row['start_time']=start_time_I;
        resultsTable_row['is_start_time']=is_start_time_I;
        resultsTable_row['end_time']=end_time_I;
        resultsTable_row['is_end_time']=is_end_time_I;
        resultsTable_row['total_width']=total_width_I;
        resultsTable_row['is_total_width']=is_total_width_I;
        resultsTable_row['width_at_50']=width_at_50_I;
        resultsTable_row['is_width_at_50']=is_width_at_50_I;
        resultsTable_row['signal_2_noise']=signal_2_noise_I;
        resultsTable_row['is_signal_2_noise']=is_signal_2_noise_I;
        resultsTable_row['baseline_delta_2_height']=baseline_delta_2_height_I;
        resultsTable_row['is_baseline_delta_2_height']=is_baseline_delta_2_height_I;
        resultsTable_row['modified_']=modified__I;
        resultsTable_row['relative_rt']=relative_rt_I;
        resultsTable_row['used_']=used__I;
        resultsTable_row['calculated_concentration']=calculated_concentration_I;
        resultsTable_row['accuracy_']=accuracy__I;
        resultsTable_row['comment_']=comment__I;
        resultsTable_row['use_calculated_concentration']=use_calculated_concentration_I;
        resultsTable_row_O = self.format_data(resultsTable_row);
        return resultsTable_row_O;

