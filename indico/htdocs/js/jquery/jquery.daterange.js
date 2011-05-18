(function($, undefined) {
    $.widget('ui.daterange', {
        // Default options
        options: {
            disabled: false,
            allowPast: false,
            fieldNames: ['startDate', 'endDate'],
            labels: ['', ''],
            labelAttrs: {},
            startDate: null,
            endDate: null,
            pickerOptions: {
                changeMonth: true,
                changeYear: true,
                firstDay: 1,
                showOtherMonths: true,
                selectOtherMonths: true,
                unifyNumRows: true,
                yearRange: '-0:+2'
            },
            startPickerOptions: {},
            endPickerOptions: {}
        },

        _create: function() {
            var self = this;

            // Create the hidden fields containing the dates
            self.startDateField = $('<input/>', {
                type: 'hidden',
                name: self.options.fieldNames[0],
                value: self.startDate || ''
            }).appendTo(self.element);
            self.endDateField = $('<input/>', {
                type: 'hidden',
                name: self.options.fieldNames[1],
                value: self.endDate || ''
            }).appendTo(self.element);

            // Create the markup for the inline widget
            self.container = $('<div/>', { style: 'display: table; width: 100%;' });
            self.startDateContainer = $('<div/>', { style: 'float: left', align: 'center' }).appendTo(self.container);
            self.endDateContainer = $('<div/>', { style: 'float: left; margin-left: 10px;', align: 'center' }).appendTo(self.container);
            $('<span/>', self.options.labelAttrs).html(self.options.labels[0]).appendTo(self.startDateContainer);
            $('<span/>', self.options.labelAttrs).html(self.options.labels[1]).appendTo(self.endDateContainer);
            self.startPicker = $('<div/>').appendTo(self.startDateContainer);
            self.endPicker = $('<div/>').appendTo(self.endDateContainer);

            // We have to do attach the container to the document before creating the pickers because e.g. chrome otherwise gives them zero height
            self.element.addClass('ui-daterange').append(self.container);

            // Create the date pickers
            // The picker options first get a default minDate, then the global picker options, then the picker-specific options, then out non-overridable options
            self.startPicker.datepicker($.extend({
                minDate: self.options.allowPast ? null : 0
            }, self.options.pickerOptions, self.options.startPickerOptions, {
                altField: self.startDateField,
                defaultDate: self.options.startDate
            }));
            self.endPicker.datepicker($.extend({
                minDate: self.options.allowPast ? null : 0
            }, self.options.pickerOptions, self.options.endPickerOptions, {
                altField: self.endDateField,
                defaultDate: self.options.endDate
            }));
            self.pickers = self.startPicker.add(self.endPicker);

            // Prevent nonsense ranges
            self.pickers.datepicker('option', 'onSelect', function() {
                if(self.startPicker.datepicker('getDate') > self.endPicker.datepicker('getDate')) {
                    if(this == self.startPicker[0]) {
                        self.endPicker.datepicker('setDate', self.startPicker.datepicker('getDate'));
                    }
                    else {
                        self.startPicker.datepicker('setDate', self.endPicker.datepicker('getDate'));
                    }
                }
                self.options.startDate = self.endPicker.datepicker('getDate');
                self.options.endDate = self.endPicker.datepicker('getDate');
            });
            // Copy current date in case it was not set before
            self.options.startDate = self.endPicker.datepicker('getDate');
            self.options.endDate = self.endPicker.datepicker('getDate');
            // Disable the date picker if necessary
            if(self.options.disabled) {
                self.pickers.datepicker('disable');
            }
        },

        destroy: function() {
            this.element.removeClass('ui-daterange')
            this.startDateField.remove();
            this.endDateField.remove();
            this.pickers.datepicker('destroy');
            this.container.remove();
            $.Widget.prototype.destroy.apply(this, arguments);
        },

        _setOption: function(key, value) {
            if(key == 'disabled') {
                if(value) {
                    this.pickers.datepicker('disable');
                }
                else {
                    this.pickers.datepicker('enable');
                }
            }
            else if(key == 'allowPast') {
                this.pickers.datepicker('option', 'minDate', value ? null : 0);
            }
            else if(key == 'startDate') {
                this.startPicker.datepicker('setDate', value);
            }
            else if(key == 'endDate') {
                this.endPicker.datepicker('setDate', value);
            }

            $.Widget.prototype._setOption.apply(this, arguments);
        },

        getStartPicker: function() {
            return this.startPicker;
        },

        getEndPicker: function() {
            return this.endPicker;
        },

        getDates: function() {
            return [this.options.startDate, this.options.endDate];
        }
    });
})(jQuery);