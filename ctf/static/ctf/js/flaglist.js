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
        
        // Init mansory card grid
        $('.grid__inner').masonry({
            itemSelector: '.grid__cell',
            columnWidth: 350,
            gutter: 10
        });
    }

    this.initClick = () => {
    }

    this.initDialog = function(){
        if($('.mdc-dialog br').length > 0){
            self.dialog.open();
        }        
    }
}