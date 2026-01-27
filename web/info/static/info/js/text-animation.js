// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    const sentences = [
        "Work on your willpower",
        "Be producer not consumer",
        "Be nice to people on the come up",
        "Watch others & then do the opposite",
        "Who you know matters more than what you know",
        "Never talk behind someone's back",
        "Make more mistakes",
        "Make reversible decisions quickly",
        "Focus on one thing at a time",
        "Don’t be the best, be the only",
        "If you don’t like something then change it",
        "Work smart not hard",
        "Assume you can learn something new from everyone",
        "Never disrespect your elders",
        "Don’t be scared of change, embrace it",
        "Live in the moment, not on your phone",
        "Always pay the bill",
        "Say no if you aren’t ready",
        "Present yourself in the way you wish to be perceived",
        "Mentally prepare yourself for your loved ones dying",
        "Never take rejection personally",
        "Don’t be embarrassed to take a nap",
        "Learn from those who disagree with you",
        "Never be late",
        "Be motivated by something greater than money",
        "Be fuelled by vision not fear",
        "Stand up to bullies",
        "Use your unfair advantages",
        "Skip the flashy car",
        "Prioritise your reputation",
        "Don't compare yourself to your friends",
        "Don’t let a bad day turn into a bad week",
        "Always Pay off your credit card",
        "Any job is better than no job",
        "Never invest without doing your research",
        "Being a great storyteller can get you anything you want",
        "Don’t live your life for others",
        "Have a solid paycheck routine",
        "Start investing now",
        "The quality of your questions will shape your future success",
        "Make sure to enjoy the journey, not just focus on the destination",
        "Nothing is ever free",
        "Stop waiting to be inspired",
        "Work hard now for an easier life later",
        "Tackle the tough tasks in the morning",
        "The name of a university means absolutely nothing",
        "Look after your back",
        "Don’t stress about being different—you don’t have to fit in",
        "Choose your partner wisely"
    ];

    const textDisplay = document.getElementById('text-display');
    let currentSentenceIndex = 0;

    async function displayText() {
        try {
            while (true) {
                const currentSentence = sentences[currentSentenceIndex];

                // Display letters one by one
                for (let i = 0; i <= currentSentence.length; i++) {
                    if (textDisplay) {
                        textDisplay.textContent = currentSentence.slice(0, i);
                        await new Promise(resolve => setTimeout(resolve, 30));
                    }
                }

                // Keep the full sentence displayed for 3 seconds
                await new Promise(resolve => setTimeout(resolve, 3000));

                // Clear the text
                if (textDisplay) {
                    textDisplay.textContent = '';
                }

                // Move to next sentence
                currentSentenceIndex = (currentSentenceIndex + 1) % sentences.length;
            }
        } catch (error) {
            console.error('An error occurred:', error);
        }
    }

    // Start the animation
    displayText();
});
