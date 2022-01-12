<template>
    <div class='row'>
            <div class='col center-text'>
                    <table class="table">
                        <thead>
                        <tr>
                            <th scope="col">Power, kW</th>
                            <th scope="col">Sum Time, h</th>
                            <th scope="col">Energy Output, MWhour</th>
                            
                        </tr>
                        </thead>
                        <tbody>
                            <tr v-for="i,index in values" v-bind:key="index">
                                <th>{{i.power}}</th>
                                <td>{{TotalHours(index, Date.parse(i.toDate), Date.parse(i.fromDate))}} </td>
                                <td>{{EnergyOutput(index)}}</td>
                            </tr>
                        </tbody>
                    </table>
            </div>
        </div>
    
</template>

<script>
export default {
    name: "Table",
    props: ["modelValue"],
    computed:{
        values: {
            get(){
                return this.modelValue
            },
            set(val){
                this.$emit("update:modelValue", val)
            }

        }
    },
    methods: {
        TotalHours(index, to, from) {
            this.values[index].totalHours = (to-from)/1000/3600
            return this.values[index].totalHours
        },
        EnergyOutput(index) {
            this.values[index].energyOutput = (this.values[index].power*this.values[index].totalHours)/1000
            return this.values[index].energyOutput
        }
    }
}
</script>