import React from 'react';
import {
  ChakraProvider,
  Box,
  Text,
  VStack,
  Grid,
  extendTheme,
  CSSReset,
} from '@chakra-ui/react';
import KikuyuTTSComponent from './KikuyuTTSComponent'; // Import the KikuyuTTSComponent

// Custom theme overrides
const customTheme = extendTheme({
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
        textTransform: 'uppercase',
      },
      sizes: {
        lg: {
          fontSize: 'lg',
          px: '32px',
          py: '8px',
        },
      },
      variants: {
        solid: (props) => ({
          bg: props.colorMode === 'dark' ? 'brand.700' : 'brand.500',
          color: 'white',
        }),
      },
    },
  },
});

function App() {
  return (
    <ChakraProvider theme={customTheme}>
      <CSSReset />
      <Box textAlign="center" fontSize="xl">
        <Grid minH="100vh" p={3}>
          <VStack spacing={8}>
            <Box>
              <Text fontSize="4xl" fontWeight="bold" color="brand.700">
                Kikuyu Text-to-Speech Converter
              </Text>
              <Text fontSize="lg" color="gray.600">
                Easily convert your text into natural-sounding Kikuyu speech.
              </Text>
            </Box>
            <KikuyuTTSComponent /> {/* Use the KikuyuTTSComponent */}
          </VStack>
        </Grid>
      </Box>
      <Box p={5} color="gray.600" borderTopWidth={1} borderColor="gray.200">
        <Text align="center">
          © 2024 Kikuyu TTS Project. All rights reserved.
        </Text>
      </Box>
    </ChakraProvider>
  );
}

export default App;
