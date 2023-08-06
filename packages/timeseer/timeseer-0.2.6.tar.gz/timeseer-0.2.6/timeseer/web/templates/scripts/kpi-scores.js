(function () {
  var kpiScores = {{ kpi_scores|tojson }};
  var comparisonKpiScores = {{ comparison_kpi_scores|tojson }}
  var kpis = {{ kpis|sort(attribute='name')|map(attribute='name')|list|tojson }};
  var dataName = {{ source_name|tojson }}
  {% if flow %}
  dataName = {{ flow.name|tojson }};
  {% endif %}

  var scores = kpis.map(function (kpi) {return kpiScores[kpi]||0;});
  var comparisonScores = kpis.map(function (kpi) {return comparisonKpiScores[kpi];});

  var data = [{
      type: 'scatterpolar',
      r: scores,
      theta: kpis,
      fill: 'toself',
      name: dataName
    },
    {
      type: 'scatterpolar',
      r: comparisonScores,
      theta: kpis,
      fill: 'toself',
      name: '{{ compare_to }}'
    }].reverse();

  var layout = {
    polar: {
      radialaxis: {
        visible: true,
        range: [0, 100]
      }
    },
    showlegend: true,
    legend: {
      y: 1.2
    },
    margin: {
      t: 0,
      l: 15,
      r: 0,
      b: 30,
    }
  }

  Plotly.newPlot("timeseries_source_score", data, layout);
})();
