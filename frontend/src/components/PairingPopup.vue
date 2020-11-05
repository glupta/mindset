<template>
  <div class="popup-window-pairing">
    <div class="popup-window">
      <div class="popup-header">
        <p class="title">PAIRING IN PROGRESS</p>
        <!--img
          alt="icons-xmark"
          class="icons-xmark"
          src="https://static.overlay-tech.com/assets/08689fdc-2beb-4e94-a37d-66212dd4a5e1.svg"
        /-->
      </div>
      <div class="popup-body">
        <p class="body">
          Habits are easier to build when they’re built with others – congrats on taking the first step!
          <br><br>
          We’ll notify you once you’ve been matched with a partner. Look out for a text message from us soon.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PairingPopup"
};
</script>

<style scoped>
.popup-window-pairing {
  display: flex;
  align-items: flex-start;
  position: absolute;
  top: 160px;
  bottom: 160px;
}
.popup-window {
  position: relative;
  border-radius: 15px;
  box-shadow: 0px -3px 7px 0px rgba(52, 52, 52, 0.23);
  display: flex;
  align-items: flex-start;
  flex-direction: column;
  align-items: center;
  background: linear-gradient(
    159deg,
    rgba(245, 247, 250, 1) 34%,
    rgba(245, 247, 250, 1) 99%
  );
  border: 1px solid rgba(54, 69, 135, 0.11);
  width: 336px;
  height: 100%;
}
.popup-header {
  background-color: rgba(255, 255, 255, 1);
  border-radius: 15px 15px 0 0;
  box-shadow: 0px 3px 6px 0px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 56px;
  border: 1px solid rgba(151, 151, 151, 0.16);
}
.title {
  font-family: "Catamaran";
  font-size: 18px;
  font-weight: 600;
  line-height: normal;
  color: rgba(38, 49, 82, 1);
  text-align: center;
  letter-spacing: 2px;
}
.popup-body {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.body {
  width: 300px;
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  text-align: center;
  opacity: 0.7;
  letter-spacing: 1px;
}
.icons-xmark {
  width: 24px;
  height: 24px;
}
</style>