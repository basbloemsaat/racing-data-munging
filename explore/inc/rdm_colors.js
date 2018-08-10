var team_colors = {
    "2018": {
        "ferrari": "#DC0000",
        "force_india": "#F596C8",
        "haas": "#5A5A5A",
        "mclaren": "#FF8700",
        "mercedes": "#00D2BE",
        "red_bull": "#00327D",
        "renault": "#FFF500",
        "sauber": "#9B0000"
        "toro_rosso": "#0032FF",
        "williams": "#EEEEEE",
    },
    "fallback": {
        "ferrari": "#FF2800",
        "unknown": "#444444",
    },
};


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