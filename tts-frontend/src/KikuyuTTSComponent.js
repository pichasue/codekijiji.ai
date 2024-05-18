import React, { useState } from 'react';
import { Input, Button, Box, useToast, Spinner, Text, VStack, Heading } from '@chakra-ui/react';

const KikuyuTTSComponent = () => {
  const [text, setText] = useState('');
  const [audioUrl, setAudioUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();

  const handleTextChange = (event) => {
    setText(event.target.value);
  };

  const handleTTSSubmit = async () => {
    if (!text.trim()) {
      toast({
        title: 'Error',
        description: "Text input can't be empty",
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setIsLoading(true);
    const ttsServiceUrl = 'https://mediavestpr.co.ke/api/tts';
    try {
      const response = await fetch(ttsServiceUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const blob = await response.blob();
      const audioUrl = URL.createObjectURL(blob);
      setAudioUrl(audioUrl);
      toast({
        title: 'Success',
        description: 'Speech generated successfully',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      console.error('Error submitting text for TTS processing:', error);
      toast({
        title: 'Error',
        description: 'Failed to generate speech',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = () => {
    const link = document.createElement('a');
    link.href = audioUrl;
    link.download = 'kikuyu_tts_output.wav';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <VStack spacing={5}>
      <Heading as="h1" size="xl" textAlign="center" my={4}>
        Kikuyu Text-to-Speech Converter
      </Heading>
      <Text textAlign="center">
        Enter the text you would like to convert to speech in the Kikuyu language.
      </Text>
      <Box w="full" maxW="md">
        <Input
          type="text"
          value={text}
          onChange={handleTextChange}
          placeholder="Enter Kikuyu text here"
          size="lg"
        />
        <Button
          onClick={handleTTSSubmit}
          isLoading={isLoading}
          loadingText="Generating..."
          colorScheme="blue"
          my={4}
          w="full"
        >
          Generate Speech
        </Button>
        {isLoading && (
          <Spinner size="xl" />
        )}
        {audioUrl && (
          <>
            <audio controls src={audioUrl}>
              Your browser does not support the audio element.
            </audio>
            <Button
              onClick={handleDownload}
              colorScheme="green"
              my={4}
              w="full"
            >
              Download Audio
            </Button>
          </>
        )}
      </Box>
    </VStack>
  );
};

export default KikuyuTTSComponent;
