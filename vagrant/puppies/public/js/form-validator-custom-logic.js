/**
 * jQuery Form Validator Module: Custom Logic
 * ------------------------------------------
 * Created by 
 * for jQuery Form Validator by Victor Jonsson <http://www.victorjonsson.se>
 *
 * Allows for searching in checkbox array values for dependencies
 *
 * - data-validation-depends-on-array
 *
 * @website http://formvalidator.net/#logic
 * @license MIT
 */
(function($) {

	'use strict';
(function($) {

	'use strict';

  var setupValidationDependsOn = function($form, conf) {

      var dependingOnBeforeValidation = function() {

          var $input = $(this),
            nameOfDependingInput = $input.valAttr('depends-on') || $input.valAttr('if-checked');

          // Whether or not this input should be validated depends on if another input has a value
          if (nameOfDependingInput) {

            // Set the boolean telling us that the validation depends
            // on another input being checked
            var valueOfDependingInput = $.formUtils.getValue('[name="' + nameOfDependingInput + '"]', $form),
              listWithRequiredValues = $.split($input.valAttr('depends-on-value'), false, false),
              dependingInputIsMissingValueOrHasIncorrectValue = !valueOfDependingInput || (
                  listWithRequiredValues.length &&
                    !valueIsInList(valueOfDependingInput, listWithRequiredValues)
                );

            if (dependingInputIsMissingValueOrHasIncorrectValue) {
              $input.valAttr('skipped', '1');
            }
          }
        },
        valueIsInList = function(value, valueList) {
          var isInList = false,
            lowerCaseValue = value.toLocaleLowerCase();

          $.each(valueList, function(i, otherValue) {
            if (lowerCaseValue === otherValue.toLocaleLowerCase()) {
              isInList = true;
              return false;
            }
          });
          return isInList;
        },
        dependingOnValueChanged = function() {
          var $input = $(this),
            $otherInput = this.$dependingInput,
            valueOfDependingInput = $.formUtils.getValue($input),
            requiredValueOfDependingInput = $input.valAttr('depending-value'),
            otherInputHasValue = $.formUtils.getValue($otherInput) ? true:false,
            dependingInputIsMissingValueOrHasIncorrectValue = !valueOfDependingInput || (
                requiredValueOfDependingInput &&
                requiredValueOfDependingInput !== valueOfDependingInput
              );

          if (dependingInputIsMissingValueOrHasIncorrectValue && !otherInputHasValue) {
            $.formUtils.dialogs.removeInputStylingAndMessage($otherInput, conf);
          }
        };

      $form.find('[data-validation-depends-on]')
        .off('beforeValidation', dependingOnBeforeValidation)
        .on('beforeValidation', dependingOnBeforeValidation)
        .each(function() {
          // Remove validation when on depending input
          var $dependingInput = $(this);
          $form.find('[name="'+$dependingInput.valAttr('depends-on')+'"]').each(function() {
            $(this)
              .off('change', dependingOnValueChanged)
              .on('change', dependingOnValueChanged)
              .valAttr('depending-value', $dependingInput.valAttr('depends-on-value'));

            this.$dependingInput = $dependingInput;

          });

        });

    },
    setupValidationTogetherWith = function($form, conf) {

      var optionalBeforeValidation = function() {
          var $input = $(this),
            dependingInputs = $input.valAttr('optional-if-answered'),
            dependingInputsHasValue = false,
            thisInputHasAnswer = $.formUtils.getValue($input) ? true:false;

          if (!thisInputHasAnswer) {
            $.each($.split(dependingInputs), function(i, inputName) {
              var $dependingInput = $form.find('[name="'+inputName+'"]');
              dependingInputsHasValue = $.formUtils.getValue($dependingInput) ? true:false;
              if (dependingInputsHasValue) {
                return false;
              }
            });

            if (dependingInputsHasValue) {
              $input.valAttr('skipped', 1);
            }
          }
        },
        optionalInputOnChange = function() {
          var $input = $(this),
            dependingInputs = $input.valAttr('optional-if-answered');

          $.each($.split(dependingInputs), function(i, inputName) {
            var $dependingInput = $form.find('[name="'+inputName+'"]'),
                dependingInputsHasValue = $.formUtils.getValue($dependingInput) ? true:false;
            if (!dependingInputsHasValue) {
              $.formUtils.dialogs.removeInputStylingAndMessage($dependingInput, conf);
            }
          });
        };

      $form.find('[data-validation-optional-if-answered]')
        .off('beforeValidation', optionalBeforeValidation)
        .on('beforeValidation', optionalBeforeValidation)
        .each(function() {
          $(this)
            .off('change', optionalInputOnChange)
            .on('change', optionalInputOnChange);
        });
    };

  $.formUtils.$win.bind('validatorsLoaded formValidationSetup', function(evt, $form, conf) {
    if( !$form ) {
      $form = $('form');
    }
    setupValidationDependsOn($form, conf);
    setupValidationTogetherWith($form, conf);
  });

})(jQuery);
