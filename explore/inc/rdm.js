var rdm = {};

(function() {
    this.reduce_sum = function(variable) {
        return function(a, b) {
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

    this.sortby = function(data, sort_term_function, sort_direction) {
        data.sort(function(a, b) {
            key_a = sort_term_function(a);
            key_b = sort_term_function(b);
            if (key_a > key_b) return (sort_direction == 'asc' ? 1 : -1);
            if (key_a < key_b) return (sort_direction == 'asc' ? -1 : 1);
            return 0;
        })
        return data;
    }

    this.current_sort = {
        title: "none",
        order: "unsorted",
    }

    this.loaded_data = {};


}).apply(rdm);