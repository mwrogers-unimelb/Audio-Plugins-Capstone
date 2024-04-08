#include "TestPlugin/PluginProcessor.h"
#include "TestPlugin/PluginEditor.h"

//==============================================================================
AudioPluginAudioProcessorEditor::AudioPluginAudioProcessorEditor (juce::AudioProcessor& parent, juce::AudioProcessorValueTreeState& vts)
    : AudioProcessorEditor (parent), valueTreeState (vts)
{
    setSize (800, 600);

    // define the parameters of slider object
    gainLabel.setText ("Gain", juce::dontSendNotification);
    addAndMakeVisible (gainLabel);

    addAndMakeVisible (gainSlider);
    gainAttachment.reset (new SliderAttachment (valueTreeState, "gain", gainSlider));

    // define parameters of button object
    invertButton.setButtonText ("Invert Phase");
    addAndMakeVisible (invertButton);
    invertAttachment.reset (new ButtonAttachment (valueTreeState, "invertPhase", invertButton));
}

AudioPluginAudioProcessorEditor::~AudioPluginAudioProcessorEditor()
{
}

//==============================================================================
void AudioPluginAudioProcessorEditor::paint (juce::Graphics& g)
{
    // // fill the whole window white
    // g.fillAll (juce::Colours::white);
 
    // set the current drawing colour to black
    //g.setColour (juce::Colours::black);
 
    // // set the font size and draw text to the screen
    g.setFont (15.0f);
 
    g.drawFittedText ("Channel Gain", 0, 0, getWidth(), 30, juce::Justification::centred, 1);
}

void AudioPluginAudioProcessorEditor::resized()
{
    // This is generally where you'll want to lay out the positions of any
    // subcomponents in your editor..

    // sets the position and size of the slider with arguments (x, y, width, height)
    gainSlider.setBounds(100, 100, 400, 100);

    // sets the position and size of the button
    invertButton.setBounds(100, 200, 100, 100);
}

// // Function to read and set the volume based on the slider value
// void AudioPluginAudioProcessorEditor::sliderValueChanged (juce::Slider* slider)
// {
//     processorRef.gain->operator= (gainVal.getValue());
// }

// // Function to read and set the invert phase button based on value
// void AudioPluginAudioProcessorEditor::buttonClicked (juce::Button* button)
// {
//     processorRef.invertPhase->operator= (phaseButton.getToggleState());
//     if (phaseButton.getToggleState()) {
//         phaseButton.setButtonText("Phase Invert (True)");
//     }
//     if (!phaseButton.getToggleState()) {
//         phaseButton.setButtonText("Phase Invert (False)");
//     }
// }