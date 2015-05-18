/* Remove the form view bss_city.view_partner_bluestar_city_form (moved in bss_partner_city_search */

delete from ir_ui_view where id = (
    select res_id from ir_model_data 
    where module = 'bss_city' and name = 'view_partner_bluestar_city_form'
);
delete from ir_model_data 
    where module = 'bss_city' and name = 'view_partner_bluestar_city_form'

