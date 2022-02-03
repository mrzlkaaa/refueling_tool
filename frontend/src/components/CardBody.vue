<template>
    <h5 class="card-body">Fuel Cycle №{{text}}</h5>
</template>

<script>
export default {
    name: "CardBody",
    props:["text"]
}
</script>
<style>
    .card-body {
        font-size: 16px;
    }
</style>