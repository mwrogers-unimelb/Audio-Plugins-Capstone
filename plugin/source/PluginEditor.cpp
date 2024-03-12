#include "TestPlugin/PluginProcessor.h"
#include "TestPlugin/PluginEditor.h"

//==============================================================================
AudioPluginAudioProcessorEditor::AudioPluginAudioProcessorEditor (AudioPluginAudioProcessor& p)
    : AudioProcessorEditor (&p), processorRef (p)
{
    juce::ignoreUnused (processorRef);
    // Make sure that before the constructor has finished, you've set the
    // editor's size to whatever you need it to be.
    setSize (400, 300);

    // these define the parameters of our slider object
    gainVal.setSliderStyle (juce::Slider::LinearBarVertical);
    gainVal.setRange (0.0, 1.0, 0.01);
    gainVal.setTextBoxStyle (juce::Slider::NoTextBox, false, 90, 0);
    gainVal.setPopupDisplayEnabled (true, false, this);
    gainVal.setTextValueSuffix (" Volume");
    gainVal.setValue(0.5);

    // add the listener to the slider
    gainVal.addListener (this);
 
    // this function adds the slider to the editor
    addAndMakeVisible (&gainVal);
}

AudioPluginAudioProcessorEditor::~AudioPluginAudioProcessorEditor()
{
}

//==============================================================================
void AudioPluginAudioProcessorEditor::paint (juce::Graphics& g)
{
    // fill the whole window white
    g.fillAll (juce::Colours::white);
 
    // set the current drawing colour to black
    g.setColour (juce::Colours::black);
 
    // set the font size and draw text to the screen
    g.setFont (15.0f);
 
    g.drawFittedText ("Gain", 0, 0, getWidth(), 30, juce::Justification::centred, 1);
}

void AudioPluginAudioProcessorEditor::resized()
{
    // This is generally where you'll want to lay out the positions of any
    // subcomponents in your editor..

    // sets the position and size of the slider with arguments (x, y, width, height)
    gainVal.setBounds (40, 30, 20, getHeight() - 60);
}

// Function to read and set the volume based on the slider value
void AudioPluginAudioProcessorEditor::sliderValueChanged (juce::Slider* slider)
{
    processorRef.gain->operator= (gainVal.getValue());
}