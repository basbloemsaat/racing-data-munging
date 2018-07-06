var rdm = {};

(function() {
    this.reduce_sum = function(variable) {
        return function(a, b) {
            var i = 0;
            // xx = { i++: a[variable] + b[variable] };  \\`
            // console.log(xx);

            var x = {};
            x[variable] = a[variable] + b[variable];
            return x
        };
    }
    this.reduce_min = function(variable) {
        return function(a, b) {
            var x = {};
            x[variable] = a[variable] < b[variable] ? a[variable] : b[variable];
            return x
        };
    }

    this.reduce_max = function(variable) {
        return function(a, b) {
            var x = {};
            x[variable] = a[variable] > b[variable] ? a[variable] : b[variable];
            return x
        };
    }

}).apply(rdm);