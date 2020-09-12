<template>
  <div class="button-dark"><p class="confirm">CONFIRM</p></div>
</template>

<script>
export default {
  name: "ButtonDark"
};
</script>

<style scoped>
.button-dark {
  border-radius: 19px;
  padding: 8px 38px;
  box-shadow: 0px 2px 10px 0px rgba(116, 115, 115, 0.33);
  display: flex;
  align-items: flex-start;
  cursor: pointer;
  background: linear-gradient(
    103deg,
    rgba(41, 44, 37, 1) 61%,
    rgba(104, 119, 94, 1) 125%,
    rgba(80, 88, 75, 1) 125%
  );
}
.confirm {
  width: 79px;
  font-family: "Source Sans Pro";
  font-size: 14px;
  font-weight: 600;
  line-height: 24px;
  color: rgba(239, 235, 220, 1);
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 2px;
}
</style>