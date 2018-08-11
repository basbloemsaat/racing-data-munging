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

    this.sortby = function(data, sort_term_function, sort_direction, numeric) {
        console.log(numeric)
        data.sort(function(a, b) {
            key_a = sort_term_function(a);
            key_b = sort_term_function(b);
            if(numeric) {
                key_a = parseFloat(key_a)             
                key_b = parseFloat(key_b)             
            }
            if (key_a > key_b) return (sort_direction == 'asc' ? 1 : -1);
            if (key_a < key_b) return (sort_direction == 'asc' ? -1 : 1);
            return 0;
        })
        return data;
    }

    this.svg_add_stripes = function(svg) {
        var defs = svg.append('defs');
        defs.append('pattern')
            .attr('id', 'pattern-stripe')
            .attr('width', 4)
            .attr('height', 4)
            .attr('patternUnits', 'userSpaceOnUse')
            .attr('patternTransform', 'rotate(45)')
            .append('rect')
            .attr('width', 2)
            .attr('height', 4)
            .attr('transform', 'translate(0,0)')
            .attr('fill', 'white');
        defs.append('mask')
            .attr('id', 'mask-stripe')
            .append('rect')
            .attr('x', 0)
            .attr('y', 0)
            .attr('width', '100%')
            .attr('height', '100%')
            .attr('fill', 'url(#pattern-stripe)');
    }

    this.current_sort = {
        title: "none",
        order: "unsorted",
    }

    this.loaded_data = {};
    
    var url_string = window.location.href;
    this.url = new URL(url_string);

}).apply(rdm);