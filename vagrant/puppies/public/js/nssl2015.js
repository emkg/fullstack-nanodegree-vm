// menu-navigation bar dropdown menus

jQuery(document).ready(function()
{
    jQuery("#bottom-menu-items").accessibleDropDown();
});

jQuery.fn.accessibleDropDown = function ()
{
    var el = jQuery(this);

    /* Setup dropdown menus for IE 6 */

    jQuery("li", el).mouseover(function() {
        jQuery(this).addClass("hover");
    }).mouseout(function() {
        jQuery(this).removeClass("hover");
    });

    /* Make dropdown menus keyboard accessible */

    jQuery("a", el).focus(function() {
        jQuery(this).parents("li").addClass("hover");
    }).blur(function() {
        jQuery(this).parents("li").removeClass("hover");
    });
}