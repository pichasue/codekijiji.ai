import React, { useState, useEffect } from 'react';
import {
  ChakraProvider,
  Box,
  Text,
  VStack,
  extendTheme,
  Button,
  FormControl,
  FormLabel,
  Textarea,
  useToast,
  useColorMode,
  IconButton,
  Image,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
} from '@chakra-ui/react';
import { uploadData } from 'aws-amplify/storage';
import { FaSun, FaMoon } from 'react-icons/fa';
import { Amplify } from 'aws-amplify';
import awsExports from './aws-exports';

Amplify.configure(awsExports);

// Custom theme colors
const customTheme = extendTheme({
  initialColorMode: 'light',
  useSystemColorMode: false,
  colors: {
    brand: {
      900: '#1a365d',
      800: '#153e75',
      700: '#2a69ac',
    },
  },
  components: {
    Button: {
      baseStyle: {
        fontWeight: 'bold',
      },
    },
  },
});

function App() {
  const [textData, setTextData] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  // const [audioBlob, setAudioBlob] = useState(null); // Commented out for testing purposes
  const [isPolicyModalOpen, setPolicyModalOpen] = useState(false);
  const toast = useToast();
  const { colorMode, toggleColorMode, setColorMode } = useColorMode();

  useEffect(() => {
    const savedColorMode = localStorage.getItem('colorMode');
    if (savedColorMode) {
      setColorMode(savedColorMode);
    }
  }, [setColorMode]);

  const handleToggleColorMode = () => {
    toggleColorMode();
    const newColorMode = colorMode === 'light' ? 'dark' : 'light';
    localStorage.setItem('colorMode', newColorMode);
  };

  const handleTextChange = (e) => setTextData(e.target.value);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      setMediaRecorder(recorder);
      // recorder.ondataavailable = (e) => setAudioBlob(e.data); // Commented out for testing purposes
      recorder.start();
      setIsRecording(true);
    } catch (error) {
      toast({
        title: 'Error accessing your microphone',
        description: 'Please ensure you have given the necessary permissions.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      setIsRecording(false);
    }
  };

  const handleSubmit = async () => {
    if (textData) {
      try {
        // Upload text data as a file
        const textFileName = `textData-${Date.now()}.txt`;
        const textFile = new Blob([textData], { type: 'text/plain' });
        await uploadData(textFileName, textFile, {
          contentType: 'text/plain'
        });

        // Display a toast on successful submission for user feedback
        toast({
          title: 'Data submitted successfully.',
          description: 'Your text data has been uploaded.',
          status: 'success',
          duration: 5000,
          isClosable: true,
        });

        // Clear the form
        setTextData('');
        // setAudioBlob(null); // Commented out for testing purposes
      } catch (error) {
        toast({
          title: 'Submission failed.',
          description: 'There was an error uploading your data.',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      }
    } else {
      toast({
        title: 'Missing data.',
        description: 'Please provide text data.',
        status: 'warning',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const togglePolicyModal = () => setPolicyModalOpen(!isPolicyModalOpen);

  return (
    <ChakraProvider theme={customTheme}>
      <Box position="relative" textAlign="center" fontSize="xl" minHeight="100vh" py={10}>
        <Image src="/home/ubuntu/browser_downloads/lady_cat_7.jpg" alt="Cultural Hut" opacity={colorMode === 'light' ? "0.5" : "0.7"} position="absolute" top="0" left="0" width="full" height="full" objectFit="cover" zIndex="-1" />
        <Box position="absolute" bottom="3" right="3" zIndex="2">
          <Image src="/home/ubuntu/browser_downloads/susan_signature.jpg" alt="Susan Ngatia's Signature" opacity="0.6" />
        </Box>
        <Box bg={colorMode === 'light' ? 'white' : 'brand.800'} color={colorMode === 'light' ? 'brand.800' : 'white'}>
          <VStack spacing={8}>
            <IconButton icon={colorMode === 'light' ? <FaMoon /> : <FaSun />} isRound="true" size="lg" alignSelf="flex-end" m={4} onClick={handleToggleColorMode} />
            <Text fontSize="3xl" fontWeight="bold">Welcome to CodeKiiJiji Data Collection Interface</Text>
            <Text fontSize="md">
              Please submit text data and voice recordings for the Kenyan languages.
            </Text>
            <FormControl id="text-data-form">
              <FormLabel>Text Data</FormLabel>
              <Textarea
                value={textData}
                onChange={handleTextChange}
                placeholder="Enter text data here"
                size="sm"
              />
            </FormControl>
            {isRecording ? (
              <Button onClick={stopRecording} colorScheme="red" size="lg">
                Stop Recording
              </Button>
            ) : (
              <Button onClick={startRecording} colorScheme="green" size="lg">
                Start Recording
              </Button>
            )}
            <Button
              onClick={handleSubmit}
              colorScheme="brand"
              size="lg"
              isDisabled={!textData}
            >
              Submit
            </Button>
            <Button onClick={togglePolicyModal} colorScheme="blue" size="sm" mt={4}>
              View Data User Policy and Privacy Policy
            </Button>
            <Modal isOpen={isPolicyModalOpen} onClose={togglePolicyModal}>
              <ModalOverlay />
              <ModalContent>
                <ModalHeader>Data User Policy and Privacy Policy</ModalHeader>
                <ModalCloseButton />
                <ModalBody>
                  <Text fontSize="md">
                    The data collected through this interface will be used solely for the purpose of developing and improving language learning models for Kenyan languages. We are committed to maintaining the privacy and security of your submissions.
                  </Text>
                  <Text fontSize="md" mt={4}>
                    By submitting your text and voice recordings, you grant us permission to use the data for research and development purposes. Your submissions will be anonymized and will not be shared with third parties without your explicit consent.
                  </Text>
                </ModalBody>
                <ModalFooter>
                  <Button colorScheme="blue" mr={3} onClick={togglePolicyModal}>
                    Close
                  </Button>
                </ModalFooter>
              </ModalContent>
            </Modal>
          </VStack>
        </Box>
      </Box>
    </ChakraProvider>
  );
}

export default App;
