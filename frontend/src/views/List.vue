<template>
    <div class="container">
        <div class="row">
            <div id="l" class="col col-3">
            1 of 2
            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
            <br>
            <div class="card text-center">
                <div class="card-header">
                    22.10.2021
                </div>
                <div class="card-body">
                    FC 122
                </div>
            </div>
            <br>
            <div class="card text-center">
                <div class="card-header">
                    24.09.2021
                </div>
                <div class="card-body">
                    FC 121
                </div>
            </div>
            <br>
            </div>
            <div id="r" class="col col-lg-8">
            2 of 2
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "List",
}
</script>
<style>
    .container {
        margin-top: 60px;
    }

    #r {
        background-color: blue
    }
    #l {
        background-color:red
    }
</style>