/**
 * Created by mahe1705 on 13.06.2017.
 */

// Funksjoner
function tegnBane() { // tegner opp banen
    console.log("Tegner opp banen");
    ctx.fillStyle=bane.gressfarge; // farge på banen
    ctx.fillRect(0,0,bane.bredde,bane.hoyde); // koordinatene til rektangelet
    ctx.fillStyle=bane.linjefarge;  // fargen til midlinjen
    // Tegner hvit linje som et rektangel der x-koordinat starter på banebredde/2 og y-koordinat på null
    ctx.fillRect(bane.bredde/2 - bane.linjetykkelse/2,0,bane.linjetykkelse,bane.hoyde);
}
function tegnBall() {
    console.log("Tenger opp ballen");
    ctx.fillStyle=ball.farge;
    ctx.fillRect(ball.xpos,ball.ypos,ball.bredde,ball.bredde);  // starter ballen i
    ball.xpos=ball.xpos+ball.xfart*ball.xretning; // Endrer x-posisjonen
    ball.ypos=ball.ypos+ball.yfart*ball.yretning; // Endrer y-posisjonen
}
function tegnRacket() {
    console.log("tegner opp racketen");
    ctx.fillStyle = racket.farge;
    ctx.fillRect(racket.xpos,racket.ypos,racket.bredde,racket.hoyde); // tegner racket som rektangel
    if(racket.ypos <= 0 && racket.yretning === -1) {    // på vei opp med racket
        return; // avslutter funksjonen
    }
    if(racket.ypos + racket.hoyde >= bane.hoyde && racket.yretning === 1) { // på vei nedover med racket
        return; // avslutter funksjonen
    }
    racket.ypos=racket.ypos + (racket.yfart*racket.yretning); // Endrer y-posisjonen
    console.log("YPOS: " + racket.ypos);
}
function tegnMotspiller() {
    ctx.fillStyle=motspiller.farge;
    ctx.fillRect(motspiller.xpos,motspiller.ypos,motspiller.bredde,motspiller.hoyde);
    if(motspiller.ypos <= 0 && motspiller.yretning === -1) {    // på vei opp med motspiller
        return; // avslutter funksjonen
    }
    if(motspiller.ypos + motspiller.hoyde >= bane.hoyde && motspiller.yretning === 1) { // på vei nedover med motspiller
        return; // avslutter funksjonen
    }
    motspiller.ypos=motspiller.ypos + (motspiller.yfart*motspiller.yretning); // Endrer y-posisjonen
}
function sjekkOmBallTrefferVegg() {
    console.log("Sjekker om ballen treffer veggene");
    if(ball.ypos + ball.bredde >= bane.hoyde) { // Nedre vegg
        ball.yretning = -1; // Ballen går oppover når den har truffet nedre vegg
        //bip.play();
    }
    if(ball.ypos <= ball.bredde) { // Øvre vegg
        ball.yretning = 1; // Ballen skal gå nedover etter at den har truffet øvre vegg
        //bip.play();
    }
}
function sjekkOmBallTrefferRacket() { // Sjekker om ballen samtidig IKKE er i de fire retningene rundt racketen samtidig
    console.log("Sjekker om ballen treffer racket");
    var ballenErTilVenstre = ball.xpos + ball.bredde < racket.xpos;
    var ballenErTilHoyre = ball.xpos - ball.bredde > racket.xpos + racket.bredde;
    var ballenErOver = ball.ypos + ball.bredde < racket.ypos;
    var ballenErunder = ball.ypos - ball.bredde > racket.ypos + racket.hoyde;
    if(!ballenErTilVenstre && !ballenErTilHoyre && !ballenErOver && !ballenErunder) {
        ball.xretning = -1; // snu retningen på ballen mot venstre
        //bip.play();
        // Må sjekke om poengene kommer fra treff på racket (tar lang tid) eller fra sprett i hjørnene (tar kort tid)
        t1 = performance.now(); // sjekker tiden siden forrige timer
        if(t1-t0 >= 50) {   // hvis tiden er større enn 50 ms kan man få poeng
            tellerPlayer1++;
            teller++;
            t0 = performance.now(); // resetter timeren
        }
        document.getElementById("player1").innerHTML=tellerPlayer1 + " points";
        if(teller%5 === 0) {
            ball.xfart += 2;
            ball.yfart +=1;
        }
    }
}
function sjekkOmBallTrefferMotspiller() { // Sjekker om ballen samtidig IKKE er i de fire retningene rundt motspiller samtidig
    console.log("Sjekker om ballen treffer motspiller");
    var ballenErTilVenstre = ball.xpos + ball.bredde < motspiller.xpos;
    var ballenErTilHoyre = ball.xpos - ball.bredde > motspiller.xpos + motspiller.bredde;
    var ballenErOver = ball.ypos + ball.bredde < motspiller.ypos;
    var ballenErunder = ball.ypos - ball.bredde > motspiller.ypos + motspiller.hoyde;
    if(!ballenErTilVenstre && !ballenErTilHoyre && !ballenErOver && !ballenErunder) {
        ball.xretning = 1; // snu retningen på ballen mot høyre
        //bip.play();
        // Må sjekke om poengene kommer fra treff på racket (tar lang tid) eller fra sprett i hjørnene (tar kort tid)
        t1 = performance.now(); // sjekker tiden siden forrige timer
        if(t1-t0 >= 50) {   // hvis tiden er større enn 50 ms kan man få poeng
            teller++;
            tellerPlayer2++;
            t0 = performance.now(); // resetter timeren
        }
        document.getElementById("player2").innerHTML=tellerPlayer2 + " points";
        if(teller%5 === 0) {   // øke vanskelighetsgrad for hvert 10. treff
            ball.xfart += 2;
            ball.yfart +=1;
        }
    }
}
function sjekkOmBallErUtenforBanen() {
    console.log("Sjekker om ballen er utenfor banen");
    if(ball.xpos > bane.bredde + ball.bredde) {     // utenfor på høyre
        theGameIsOn = false;
        gameOver();
    }
    if(ball.xpos < 0) {    // utenfor på venstre
        theGameIsOn = false;
        gameOver();
    }
}

function gameOver() {
    var overskrift = document.getElementById("midtTekst");
    var player1 = document.getElementById("player1");
    var player2 = document.getElementById("player2");
    overskrift.innerHTML="GAME OVER!";
    overskrift.style.color= "red";
    //player1.style.visibility = "hidden";   // gjør teksten usynlig
    //player2.style.visibility = "hidden";
}




