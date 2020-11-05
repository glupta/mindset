<template>
  <div class="home-wellnesscard-multi">
    <div class="relative-wrapper1">
      <div class="headercolor">
        <p class="cardtitle">Habit #1</p>
      </div>
    </div>
    <div class="flex-wrapper1">
      <div class="home-wellnesshabit-piegraph">
        <img
          alt="path"
          class="path1"
          src="https://static.overlay-tech.com/assets/0bb444fb-5d1f-4390-b586-e9e72b2379a2.svg"
        />
      </div>
      <p class="num-7-8">{{habit_val}} / 1</p>
    </div>
    <p class="habit">{{habit_name}}</p>
    <div v-if="complete_bool" class="home-wellnesshabit-complete" @click="onSelectComplete">
      <p class="complete">COMPLETE</p>
    </div>
    <div v-if="check_bool" class="forgotpassword-success">
      <div class="icons-checkmark">
        <img
          alt="icons-check"
          class="icons-check"
          src="https://static.overlay-tech.com/assets/dbc04bcd-741e-42f5-97f6-6f02e5a162bc.png"
        />
      </div>
    </div>
    <!--div class="home-wellnesshabit-number">
      <div class="relative-wrapper1">
        <div class="entrybox"></div>
        <p class="entrytext">Count</p>
      </div>
      <div class="plus">
        <img
          alt="path"
          class="path2"
          src="https://static.overlay-tech.com/assets/2e11d434-6603-48f4-93f3-d4eb0f06a28c.svg"
        />
      </div>
    </div-->
  </div>
</template>

<script>
export default {
  name: "HomeWellnessCard",
  data () {
    return {
      habit_name: "",
      complete_bool: false,
      check_bool: false,
      habit_val: ""
    }
  },
  props: {
    sessionHash: String,
    dataEntry: Boolean,
    selectedDate: Date,
  },
  mounted() {
    this.updateCard();
  },
  watch: {
    sessionHash(newValue) {
      this.updateCard();
    },
    selectedDate(newValue) {
      console.log("selected date:",this.selectedDate);
      this.updateCard();
    },
    dataEntry(newValue) {
      this.updateCard();
    }
  },
  methods: {
    updateCard() {
      console.log("hash:",this.sessionHash,"dataEntry:",this.dataEntry);

      //get hash habit & hash data
      if (this.sessionHash && this.selectedDate) {
        //let offset = new Date().getTimezoneOffset();
        console.log("selected date:",this.selectedDate);
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
.home-wellnesscard-multi {
  background-color: rgba(255, 255, 255, 1);
  border-radius: 18px;
  padding: 0px 0px 15px;
  box-shadow: 0px 3px 6px 0px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  border: 1px solid rgba(151, 151, 151, 0.16);
}
.relative-wrapper1 {
  margin-bottom: 16px;
  display: flex;
  align-items: flex-start;
  position: relative;
}
.headercolor {
  width: 174px;
  height: 32px;
  background-color: rgba(247, 195, 79, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.cardtitle {
  font-family: "Source Sans Pro";
  font-size: 14px;
  font-weight: 600;
  line-height: normal;
  color: rgba(255, 255, 255, 1);
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 2px;
}
.flex-wrapper1 {
  margin-bottom: 20px;
  padding: 0px 0px 0px 16px;
  display: flex;
  flex-direction: row;
  align-items: center;
}
.num-7-8 {
  width: 46px;
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 400;
  line-height: normal;
  color: rgba(38, 49, 82, 1);
  text-align: center;
  letter-spacing: 2px;
}
.habit {
  width: 114px;
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  margin-bottom: 7px;
  margin-left: 16px;
  letter-spacing: 1px;
}

/* wellness habit pie */
.home-wellnesshabit-piegraph {
  border-radius: 50%;
  padding: 3px 3px 3px 9px;
  display: flex;
  align-items: flex-start;
  border: 1px solid rgba(249, 174, 6, 1);
  margin-right: 32px;
}
.path1 {
  width: 36px;
  height: 42px;
}

/* wellness habit number */
.home-wellnesshabit-number {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-left: 15px;
}
.entrybox {
  width: 72px;
  height: 38px;
  background-color: rgba(255, 255, 255, 1);
  border-radius: 5px;
  position: relative;
  border: 1px solid rgba(37, 49, 85, 0.3);
}
.entrytext {
  width: 69px;
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
  position: absolute;
  right: -5px;
  top: 8px;
  letter-spacing: 1px;
}
.plus {
  padding: 7px 7px 8px 8px;
  display: flex;
  align-items: flex-start;
  background-image: url("https://static.overlay-tech.com/assets/57fde2a0-663a-4d38-832e-01aa7e4bec0f.png");
}
.path2 {
  width: 9px;
  height: 9px;
}

/* complete button */
.home-wellnesshabit-complete {
  margin-left: 16px;
  border-radius: 12px;
  padding: 10px 6px 10px 6px;
  box-shadow: 0px 3px 5px 0px rgba(48, 48, 48, 0.15);
  display: flex;
  align-items: flex-start;
  background: linear-gradient(
    332deg,
    rgba(37, 49, 85, 1) 14%,
    rgba(76, 95, 142, 1) 86%,
    rgba(76, 95, 142, 1) 86%
  );
  cursor: pointer;
}
.complete {
  width: 105px;
  font-family: "Catamaran";
  font-size: 13px;
  font-weight: 500;
  line-height: normal;
  color: rgba(255, 255, 255, 1);
  text-align: center;
  letter-spacing: 1px;
}

/* check mark */
.forgotpassword-success {
  margin-left: 16px;
  border-radius: 50%;
  padding: 8px;
  display: flex;
  align-items: flex-start;
  border: 6px solid rgba(89, 215, 86, 1);
}
.icons-checkmark {
  padding: 6px 3px 5px;
  display: flex;
  align-items: flex-start;
}
.icons-check {
  width: 18px;
  height: 13px;
}
</style>