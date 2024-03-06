#include <gtest/gtest.h>
#include <TestPlugin/PluginProcessor.h>

// Base test format (expected failure) - tests if audio project complies and runs fine
namespace audio_plugin_test {
TEST(AudioPlugin, Foo) {
    AudioPluginAudioProcessor processor();
    ASSERT_FALSE(true);
}
}
