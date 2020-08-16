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
        self.dialog = new mdc.dialog.MDCDialog(document.querySelector('.mdc-dialog'));
    }

    this.initClick = () => {
        // $('.flag-submit .mdc-button').on('click', function(){
        //     $('#flag-submit-form').submit();
        // });
    }

    this.initDialog = function(){
        if($('.mdc-dialog br').length > 0){
            self.dialog.open();
        }        
    }
}