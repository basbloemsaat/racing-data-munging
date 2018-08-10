(function() {
    this.team_color = function(ref, year) {
        if (team_colors[year] && team_colors[year][ref]) {
            return team_colors[year][ref];
        }
        if (team_colors["fallback"][ref]) {
            return team_colors["fallback"][ref];
        }
        return team_colors["fallback"]["unknown"];
    }
}).apply(rdm);

var team_colors = {
    "2018": {
        "ferrari": "#DC0000",
        "force_india": "#F596C8",
        "haas": "#5A5A5A",
        "mclaren": "#FF8700",
        "mercedes": "#00D2BE",
        "red_bull": "#00327D",
        "renault": "#FFF500",
        "sauber": "#9B0000",
        "toro_rosso": "#0032FF",
        "williams": "#EEEEEE",
    },
    "2017": {
        "ferrari": "#C30000",
        "force_india": "#FF80C7",
        "haas": "#6C0000",
        "mclaren": "#FF7B08",
        "mercedes": "#00CFBA",
        "red_bull": "#00007D",
        "renault": "#FFD800",
        "sauber": "#006EFF",
        "toro_rosso": "#0000FF",
        "williams": "#EEEEEE",
    },
    "fallback": {
        "ferrari": "#FF2800",
        "lotus": "#FFB800",
        "marussia": "#6E0000",
        "red_bull": "#4F1AAB",
        "sauber": "#0063FF",
        "toro_rosso": "#0005C1",
        "unknown": "#444444",
    },
};

