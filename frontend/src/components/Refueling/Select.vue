<template>
    <select v-model="selectedValue" @change="$emit('selected', selectedValue)" id="floatingSelect"
        class="form-select" aria-label="Floating label select">
        <option selected value>Choose any</option>
        <option v-for="(o,i) in optns" :key=i :value="o.value">
            {{o.name}}
        </option>
    </select>
</template>
<script>
export default {
    name: "Select",
    props:{
        optns: Array,
    },
    emits:["selected"],
    data(){
        return{
            selectedValue: "",
        }
    },
}
</script>