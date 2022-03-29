class MissPacman {
    constructor() {
        this.farge = "yellow";
        this.x = 100;
        this.y = 200;
        this.xretning = 1;  // Starter mot høyre
        this.yretning = 0;
        this.speed = 3;
    }
    oppdater(sirkel) {
        this.x = this.x + (this.speed * this.xretning);
        this.y = this.y + (this.speed * this.yretning);
        let bredde = window.innerWidth;
        let hoyde = window.innerHeight;
        if(this.x >= bredde) {
            // Utenfor til høyre
            this.x = 0 - 70;
        }
        this.draw(sirkel);

    }
    draw(sirkel) {
        // Tegner opp miss pacman
        sirkel.style.left = this.x + "px";
        sirkel.style.top = this.y + "px";
    }
}