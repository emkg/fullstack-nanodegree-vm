/**
 * jQuery Form Validator Module: Date
 * ------------------------------------------
 * Created by Victor Jonsson <http://www.victorjonsson.se>
 *
 * The following validators will be added by this module:
 *  - Country
 *  - US state
 *  - longitude and latitude
 *
 * @website http://formvalidator.net/#location-validators
 * @license MIT
 */
(function($) {

    /*
     * Validate that country exists
     */
    $.formUtils.addValidator({
        name : 'country',
        validatorFunction : function(str) {
            return $.inArray(str.toLowerCase(), this.countries) > -1;
        },
        countries : ['usa','uzbekistan','vanuatu','venezuela','viet nam','virgin islands','wake island','wallis and futuna','west bank','western sahara','yemen','zambia','zimbabwe'],
        errorMessage : '',
        errorMessageKey: 'badCustomVal'
    });

    /*
     * Is this a valid federate state in the US
     */
    $.formUtils.addValidator({
        name : 'federatestate',
        validatorFunction : function(str) {
            return $.inArray(str.toLowerCase(), this.states) > -1;
        },
        states : ['alabama','alaska', 'arizona', 'arkansas','california','colorado','connecticut','delaware','florida','georgia','hawaii','idaho','illinois','indiana','iowa','kansas','kentucky','louisiana','maine','maryland', 'district of columbia', 'massachusetts','michigan','minnesota','mississippi','missouri','montana','nebraska','nevada','new hampshire','new jersey','new mexico','new york','north carolina','north dakota','ohio','oklahoma','oregon','pennsylvania','rhode island','south carolina','south dakota','tennessee','texas','utah','vermont','virginia','washington','west virginia','wisconsin','wyoming'],
        errorMessage : '',
        errorMessageKey: 'badCustomVal'
    });


    $.formUtils.addValidator({
        name : 'longlat',
        validatorFunction : function(str) {
            var regexp = /^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$/;
            return regexp.test(str);
        },
        errorMessage:'',
        errorMessageKey:'badCustomVal'
    });

    /**
     * @private
     * @param {Array} listItems
     * @return {Array}
     */
    var _makeSortedList = function(listItems) {
        var newList = [];
        $.each(listItems, function(i, value) {
            newList.push(value.substr(0,1).toUpperCase() + value.substr(1, value.length));
        });
        newList.sort();
        return newList;
    };

    $.fn.suggestCountry = function(settings) {
        var countries = _makeSortedList($.formUtils.validators.validate_country.countries),
          usaIndex = $.inArray(countries, 'Usa');

        countries[usaIndex] = 'USA';
        return $.formUtils.suggest(this, countries, settings);
    };

    $.fn.suggestState = function(settings) {
        var states = _makeSortedList($.formUtils.validators.validate_federatestate.states);
        return $.formUtils.suggest(this, states, settings);
    };

})(jQuery);
