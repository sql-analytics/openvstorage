// license see http://www.openvstorage.com/licenses/opensource/
/*global define */
define([
    'knockout', 'jquery',
    'ovs/generic'
], function(ko, $, generic) {
    "use strict";
    return function() {
        var self = this;

        self.text     = undefined;
        self.items    = ko.observableArray([]);
        self.target   = ko.observableArray([]);
        self.multi    = ko.observable(false);
        self.selected = ko.computed(function() {
            var items = [], i;
            for (i = 0; i < self.items().length; i += 1) {
                if (self.contains(self.items()[i])) {
                    items.push(self.items()[i]);
                }
            }
            return items;
        });
        self.set    = function(item) {
            if (self.multi()) {
                if (self.contains(item)) {
                    self.target.remove(item);
                } else {
                    self.target.push(item);
                }
            } else {
                self.target(item);
            }
        };
        self.contains = function(item) {
            return $.inArray(item, self.target()) !== -1;
        };

        self.activate = function(settings) {
            if (!settings.hasOwnProperty('items')) {
                throw 'Items should be specified';
            }
            if (!settings.hasOwnProperty('target')) {
                throw 'Target should be specified';
            }
            self.items = settings.items;
            self.target = settings.target;

            if (self.target.isObservableArray) {
                self.multi(true);
            } else if (self.target() === undefined && self.items().length > 0) {
                self.target(self.items()[0]);
            }
            self.text = generic.tryGet(settings, 'text', function(item) { return item; });
            self.target.valueHasMutated();
        };
    };
});