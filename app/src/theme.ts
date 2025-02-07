import { buildTheme, ICheckboxTheme, IIconButtonTheme, ITextTheme, ITheme, mergeTheme, mergeThemePartial, ThemeMap } from '@kibalabs/ui-react';

export const buildHookeTheme = (): ITheme => {
  const baseTheme = buildTheme();
  const textThemes: ThemeMap<ITextTheme> = {
    ...baseTheme.texts,
    default: mergeTheme(baseTheme.texts.default, {
      'font-family': 'Montserrat, sans-serif',
      'font-weight': '400',
    }),
    header1: {
      'font-weight': '800',
      color: '$colors.brandPrimary',
    },
    navBarLogo: {
      'font-weight': '800',
      color: 'white',
    },
    light: {
      color: '$colors.backgroundDarker50',
    },
    warning: {
      color: '$colors.warning',
    },
    header3: {
      'font-size': '1em',
      'font-weight': 'bolder',
    },
    header4: {
      'font-size': '1em',
      'font-weight': 'normal',
      'text-decoration': 'underline',
    },
  };
  const theme = buildTheme({
    colors: {
      background: '#000',
      brandPrimary: 'rgb(39, 236, 111)',
      warning: '#cf9f04',
    },
    fonts: {
      main: {
        url: 'https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&display=swap',
      },
    },
    texts: textThemes,
    buttons: {
      destructive: {
        normal: {
          default: {
            background: {
              'background-color': '$colors.error',
            },
            text: {
              color: 'white',
            },
          },
        },
      },
    },
    pills: {
      default: {
        background: {
          padding: `${baseTheme.dimensions.paddingNarrow} ${baseTheme.dimensions.paddingWide}`,
          'background-color': '$colors.backgroundDark05',
          'border-width': '0',
        },
        text: {
          'font-size': '0.7em',
        },
      },
      small: {
        background: {
          padding: `0 ${baseTheme.dimensions.paddingNarrow}`,
        },
        text: {
          'font-size': '0.5em',
        },
      },
      error: {
        background: {
          'background-color': '$colors.errorClear90',
        },
        text: {
          color: '$colors.error',
        },
      },
    },
    links: {
      note: {
        normal: {
          default: {
            text: {
              'font-size': baseTheme.texts.note['font-size'],
            },
          },
        },
      },
      large: {
        normal: {
          default: {
            text: {
              'font-size': baseTheme.texts.large['font-size'],
            },
          },
        },
      },
      plain: {
        normal: {
          default: {
            text: {
              'text-decoration': 'none',
            },
          },
        },
      },
    },
    iconButtons: {
      default: {
        disabled: {
          default: {
            background: {
              'background-color': (baseTheme.iconButtons as ThemeMap<IIconButtonTheme>).default.normal?.default.background['background-color'],
              opacity: '0.2',
            },
          },
        },
      },
      tertiary: {
        normal: {
          default: {
            text: {
              color: '$colors.textClear50',
            },
          },
        },
      },
    },
    inputWrappers: {
      default: {
        normal: {
          default: {
            background: {
              'background-color': 'transparent',
            },
          },
        },
      },
    },
    checkboxes: {
      default: {
        disabled: {
          default: {
            checkBackground: {
              'background-color': (baseTheme.checkboxes as ThemeMap<ICheckboxTheme>).default.normal.default.checkBackground['background-color'],
              opacity: '0.2',
            },
            text: {
              color: '$colors.textClear80',
            },
          },
        },
      },
    },
    boxes: {
      task: mergeThemePartial(baseTheme.boxes.card, baseTheme.boxes.unmargined, baseTheme.boxes.unpadded, {
        'background-color': 'white',
        'border-width': '0',
      }),
      navBar: {
        'background-color': '$colors.brandPrimary',
        'border-radius': '0',
        padding: baseTheme.dimensions.paddingWide,
        'box-shadow': baseTheme.boxes.card['box-shadow'],
        position: 'sticky',
        top: '0',
      },
    },
    listItems: {
      card: {
        normal: {
          default: {
            background: baseTheme.boxes.card,
          },
          hover: {
            background: {
              'background-color': '$colors.brandPrimaryClear95',
            },
          },
        },
        selected: {
          default: {
            background: {
              'background-color': '$colors.brandPrimaryClear90',
            },
          },
        },
      },
    },
    portals: {
      unpadded: {
        background: {
          padding: '0',
        },
      },
    },
  });
  return theme;
};
