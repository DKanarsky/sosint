function Flaglist() {
    const self = this;

    this.init = function(){
        self.initElements();
        self.initClick();
        self.initDialog();
    }

    this.initElements = () => {
        const selector = '.mdc-button, .mdc-card__primary-action';
        const ripples = [].map.call(document.querySelectorAll(selector), function(el) {
            return new mdc.ripple.MDCRipple(el);
        });
        const submitFields = [].map.call(document.querySelectorAll('.mdc-text-field'), function(el) {
            return new mdc.textField.MDCTextField(el);
        });        
        
        // Init mansory card grid
        $('.grid__inner').masonry({
            itemSelector: '.grid__cell',
            columnWidth: 350,
            gutter: 10,
            fitWidth: true
        });
        $('.grid__inner').removeClass('hidden');
    }

    this.initClick = () => {
        $(".mdc-dialog").on('click', '#btn-submit-answer', function(){
            $('#flag-submit-form').submit();
        })
        $(".mdc-card").on('click',function(){
            var flag_id = $(this).data("flag-id");
            $('.mdc-card[data-flag-id="'+ flag_id +'"] .flag-view-form').submit();
        })
    }

    this.initDialog = function(){
        if($('.mdc-dialog').length > 0){
            self.dialog = new mdc.dialog.MDCDialog(document.querySelector('.mdc-dialog'));
            $('#submit-answer-input').focus();
        }        
    }
}