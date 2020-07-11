new Vue({
    el: "#app",
    data: {
        downloads: null,
        dateRanges: [
          {
            from: "2019-08-26",
            to: "2019-08-31"
          },
          {
            from: "2019-08-19",
            to: "2019-08-25"
          },
          {
            from: "2019-08-12",
            to: "2019-08-18"
          },
          {
            from: "2019-08-05",
            to: "2019-08-11"
          },
          {
            from: "2019-08-01",
            to: "2019-08-04"
          }
        ],
        selectedDateRange: null,
        dateFormat: "MM/DD"
     
    },
    computed: {
      dataset() {
        return this.downloads && this.downloads.length
          ? this.downloads.map(d => d.downloads)
          : null;
      },
      xLabels() {
        return this.downloads && this.downloads.length
          ? this.downloads.map(d => moment(d.day).format(this.dateFormat))
          : [];
      }
    },
    methods: {
      onRangeChange() {
        this.fetchData();
      },
      fetchData() {
        axios
          .get(
            `https://api.npmjs.org/downloads/range/${
              this.selectedDateRange.from
            }:${this.selectedDateRange.to}/vue-trend-chart`
          )
          .then(res => {
            const { downloads } = res.data;
            this.downloads = downloads;
          })
          .catch(error => {
            console.log(error);
          });
      }
    },
    watch: {
      selectedDateRange() {
        this.fetchData();
      }
    },
    mounted() {
      this.selectedDateRange = this.dateRanges[0];
      this.fetchData();
    }
  });
  