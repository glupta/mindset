<template>
  <div class="habit-bar">
    <div class="relative-wrapper1">
      <div class="iconbox"></div>
      <div class="icon-placeholder"></div>
    </div>
    <div class="flex-wrapper1">
      <p class="meditate">{{habit_name}}</p>
      <!--div class="relative-wrapper2">
        <div class="progressbar"></div>
        <div class="rectangle"></div>
      </div-->
    </div>
    <div class="flex-wrapper2">
      <p class="num-12-of-15">{{habit_val}} of 1</p>
      <!--p class="minutes">minutes</p-->
    </div>
  </div>
</template>

<script>
export default {
  name: "HomeWellnessBar",
  data () {
    return {
      habit_name: "",
      complete_bool: false,
      check_bool: false,
      habit_val: "",
    }
  },
  props: {
    sessionHash: String,
    dataEntry: Boolean,
    selectedDate: Date,
    borderColor: String
  },
  mounted() {
    this.updateCard();
  },
  watch: {
    sessionHash(newValue) {
      this.updateCard();
    },
    selectedDate(newValue) {
      console.log("selected date card1:",this.selectedDate);
      this.updateCard();
    },
    dataEntry(newValue) {
      this.updateCard();
    },
    borderColor(newValue) {
      this.updateCard();
    }
  },
  methods: {
    updateCard() {
      console.log("hash:",this.sessionHash,"dataEntry:",this.dataEntry,"bc:",this.borderColor);

      //get hash habit & hash data
      if (this.sessionHash && this.selectedDate) {
        if (this.borderColor) {
          console.log("bc:",this.borderColor);
          //document.getElementById("headercolor").style.backgroundColor = this.borderColor;
        }
        //let offset = new Date().getTimezoneOffset();
        console.log("selected date card2:",this.selectedDate);
        fetch('/api/checkhash?h=' + this.sessionHash + '&d=' + this.selectedDate.toISOString())
        .then(response => {
          if (response.status !== 200) { //server error handling
            console.log(`Looks like there was a problem. Status code: ${response.status}`);
            return;
          }
          response.json().then(data => {
            if ('error' in data) {
              alert(data['error']);
              return;
            }
            if ('habit_name' in data) {
              if (data['habit_name']) {
                this.habit_name = data['habit_name'];
                console.log("habit name:",this.habit_name);
              }
            }
            if ('count' in data) {
              this.habit_val = data['count'];
              console.log("habit val:",this.habit_val);
              if (this.dataEntry) {
                if (this.habit_val == '0') {
                  this.complete_bool = true;
                  this.check_bool = false;
                }
                else if (this.habit_val == '1') {
                  this.complete_bool = false;
                  this.check_bool = true;
                }
              }
              else {
                this.complete_bool = false;
                this.check_bool = false;
              }
            }
          });
        })
        .catch(error => { //error handling
          console.log("Fetch error: " + error);
        });
      }
    },
    onSelectComplete() {
      //do something
      if (this.sessionHash && this.selectedDate) {
        fetch('/api/completehabit?h=' + this.sessionHash + '&d=' + this.selectedDate.toISOString())
        .then(response => {
          if (response.status !== 200) { //server error handling
            console.log(`Looks like there was a problem. Status code: ${response.status}`);
            return;
          }
          response.json().then(data => {
            if ('error' in data) {
              alert(data['error']);
              return;
            }
            if ('habit_name' in data) {
              if (data['habit_name']) {
                this.habit_name = data['habit_name'];
                console.log("habit name:",this.habit_name);
              }
            }
            if ('success' in data) {
              console.log("habit updated");
              this.complete_bool = false;
              this.check_bool = true;
              this.$emit('update-bar');
              this.updateCard();
            }
          });
        })
        .catch(error => { //error handling
          console.log("Fetch error: " + error);
        });
      }
    }
  }
};
</script>

<style scoped>
.habit-bar {
  background-color: rgba(255, 255, 255, 1);
  border-radius: 15px;
  padding: 14px 13px 15px 15px;
  box-shadow: 0px 2px 2px 0px rgba(202, 205, 216, 0.31);
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  border: 1px solid rgba(151, 151, 151, 1);
}
.relative-wrapper1 {
  margin-right: 16px;
  display: flex;
  align-items: flex-start;
  position: relative;
}
.iconbox {
  width: 51px;
  height: 51px;
  background-color: rgba(255, 255, 255, 1);
  border-radius: 10px;
  position: relative;
  border: 1px solid rgba(209, 84, 117, 1);
}
.icon-placeholder {
  width: 28px;
  height: 28px;
  background-color: rgba(209, 84, 117, 1);
  border-radius: 6px;
  position: absolute;
  right: 12px;
  bottom: 12px;
}
.flex-wrapper1 {
  padding: 4px 0px 0px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-right: 66px;
}
.flex-wrapper2 {
  padding: 4px 0px 0px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.meditate {
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 600;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  margin-bottom: 7px;
  letter-spacing: 1px;
}
.relative-wrapper2 {
  display: flex;
  align-items: flex-start;
  position: relative;
}
.progressbar {
  width: 194px;
  height: 4px;
  background-color: rgba(216, 216, 216, 1);
  border-radius: 3px;
  opacity: 0.2;
  position: absolute;
  right: -30px;
  top: 0px;
  border: 1px solid rgba(151, 151, 151, 1);
}
.rectangle {
  width: 166px;
  height: 6px;
  background-color: rgba(209, 84, 117, 1);
  border-radius: 3px;
  position: relative;
}
.num-12-of-15 {
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 600;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  text-align: right;
  margin-bottom: 1px;
  letter-spacing: 1px;
}
.minutes {
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 400;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  text-align: right;
  opacity: 0.7;
  letter-spacing: 1px;
}
</style>