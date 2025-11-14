import React, { useState, useEffect, useRef } from 'react';
import styles from './mainArchitecture.module.css';
import Input from '../../ElementUi/Input/Input';
import Select from '../../ElementUi/Select/Select';
import NumberFieldsGrid from '../../ElementUi/NumberFieldsGrid/NumberFieldsGrid';
import NumberField from '../../ElementUi/NumberField/NumberField';
import { CheckboxTrue } from '../../ElementUi/CheckboxTrue/Checkbox';
import CheckboxField from '../../ElementUi/Checkbox/CheckboxField';
import Slider from '../../ElementUi/Slider/Slider';
import { useFormSection } from '../../../contexts/FormContext';
import Buildings from './Buildings/Buildings';
import Stilobaty from './Stilobaty/Stilobaty';

interface ArchitectureFormData extends Record<string, unknown> {
  areaValue: string;
  undergroundGnsArea: string;
  undergroundVolume: string;
  undergroundStairs: string;
  undergroundSmokelessStairs: string;
  parkingFloors: string;
  parkingTiers: string;
  parkingTotalArea: string;
  parkingFireCompartments: string;
  parkingSpaces: string;
  hasCarWash: boolean;
  undergroundParkingIndex: string[] | null;
  stilobatLinkedIndex: string[] | null;
  annexLinkedIndex: string[] | null;
  buildingCount: number;
  stilobatCount: number;
  annexCount: number;
  hasTechFloor: boolean;
  hasTechAttic: boolean;
  hasBasement: boolean;
  hasGarbageChute: boolean;
  publicPremisesCount: string;
  totalPublicArea: string;
  hasQuartergraphy: boolean;
  totalApartmentArea: string;
  oneRoomCount: string;
  twoRoomCount: string;
  threeRoomCount: string;
  fourRoomCount: string;
  moreThanFourRoomCount: string;
  penthouseCount: string;
  studioCount: string;
  hasExploitedRoof: boolean;
  publicPremisesPurpose: string[] | null;
  stilobatCalculated: boolean[];
  stilobatFloors: string[];
  stilobatAvgArea: string[];
  stilobatAvgHeight: string[];
  stilobatTotalArea: string[];
  stilobatGnsArea: string[];
  stilobatVolume: string[];
  stilobatStairs: string[];
  stilobatSmokelessStairs: string[];
  stilobatLifts: string[];
  annexCalculated: boolean[];
  annexFloors: string[];
  annexArea: string[];
  annexHeight: string[];
  annexTotalArea: string[];
  annexGnsArea: string[];
  annexVolume: string[];
  annexStairs: string[];
  annexSmokelessStairs: string[];
  annexLifts: string[];
  sectionsCounts: number[];
  sectionCalculated: boolean[][];
  sectionAreas: string[][];
  sectionFloors: string[][];
  sectionFirstFloorHeight: string[][];
  sectionTypicalFloorHeight: string[][];
  sectionTotalArea: string[][];
  sectionGnsArea: string[][];
  sectionVolume: string[][];
  sectionFireHeight: string[][];
  sectionStaircases: string[][];
  sectionSmokelessStaircases: string[][];
  sectionElevators: string[][];
  undergroundCalculated: boolean;
  undergroundFloors: string;
  undergroundAvgArea: string;
  undergroundAvgHeight: string;
  undergroundStorageArea: string;
  undergroundTotalArea: string;
  hasUndergroundParking: boolean;
  objectCalculated: boolean;
  calculatedStairs: string;
  calculatedElevators: string;
  calculatedStaircases: string;
  calculatedPublicArea: string;
  calculatedPublicPurpose: string;
  calculatedPublicCount: string;
  calculatedAbovegroundVolume: string;
  calculatedResidents: string;
  calculatedUndergroundVolume: string;
  calculatedTotalArea: string;
  calculatedTotalVolume: string;
  calculatedResidentsCount: string;
}

const defaultArchitectureData: ArchitectureFormData = {
  areaValue: '',
  undergroundParkingIndex: null,
  stilobatLinkedIndex: null,
  annexLinkedIndex: null,
  buildingCount: 0,
  stilobatCount: 0,
  annexCount: 0,
  hasTechFloor: false,
  hasTechAttic: false,
  hasBasement: false,
  hasGarbageChute: false,
  publicPremisesCount: '',
  totalPublicArea: '',
  hasQuartergraphy: false,
  totalApartmentArea: '',
  oneRoomCount: '',
  twoRoomCount: '',
  threeRoomCount: '',
  fourRoomCount: '',
  moreThanFourRoomCount: '',
  penthouseCount: '',
  studioCount: '',
  hasExploitedRoof: false,
  publicPremisesPurpose: null,
  stilobatCalculated: [],
  stilobatFloors: [],
  stilobatAvgArea: [],
  stilobatAvgHeight: [],
  stilobatTotalArea: [],
  stilobatGnsArea: [],
  stilobatVolume: [],
  stilobatStairs: [],
  stilobatSmokelessStairs: [],
  stilobatLifts: [],
  annexCalculated: [],
  annexFloors: [],
  annexArea: [],
  annexHeight: [],
  annexTotalArea: [],
  annexGnsArea: [],
  annexVolume: [],
  annexStairs: [],
  annexSmokelessStairs: [],
  annexLifts: [],
  sectionsCounts: [],
  sectionCalculated: [],
  sectionAreas: [],
  sectionFloors: [],
  sectionFirstFloorHeight: [],
  sectionTypicalFloorHeight: [],
  sectionTotalArea: [],
  sectionGnsArea: [],
  sectionVolume: [],
  sectionFireHeight: [],
  sectionStaircases: [],
  sectionSmokelessStaircases: [],
  sectionElevators: [],
  undergroundCalculated: false,
  undergroundFloors: '',
  undergroundAvgArea: '',
  undergroundAvgHeight: '',
  undergroundStorageArea: '',
  undergroundTotalArea: '',
  hasUndergroundParking: false,
  objectCalculated: false,
  calculatedStairs: '',
  calculatedElevators: '',
  calculatedStaircases: '',
  calculatedPublicArea: '',
  calculatedPublicPurpose: '',
  calculatedPublicCount: '',
  calculatedAbovegroundVolume: '',
  calculatedResidents: '',
  calculatedUndergroundVolume: '',
  calculatedTotalArea: '',
  calculatedTotalVolume: '',
  calculatedResidentsCount: '',
  undergroundGnsArea: '',
  undergroundVolume: '',
  undergroundStairs: '',
  undergroundSmokelessStairs: '',
  parkingFloors: '',
  parkingTiers: '',
  parkingTotalArea: '',
  parkingFireCompartments: '',
  parkingSpaces: '',
  hasCarWash: false
};

export default function MainArchitecture() {
  const { data, setData } = useFormSection<ArchitectureFormData>('architecture', defaultArchitectureData);
  const isHydrated = useRef(false);
  const [areaValue, setAreaValue] = useState<string>('');
  
  const [undergroundParkingIndex, setUndergroundParkingIndex] = useState<string[] | null>(null);
  const [stilobatLinkedIndex, setStilobatLinkedIndex] = useState<string[] | null>(null);
  const [annexLinkedIndex, setAnnexLinkedIndex] = useState<string[] | null>(null);
  
  const [buildingCount, setBuildingCount] = useState(0);
  const [stilobatCount, setStilobatCount] = useState(0);
  const [annexCount, setAnnexCount] = useState(0);
  const [hasTechFloor, setHasTechFloor] = useState(false);
  const [hasTechAttic, setHasTechAttic] = useState(false);
  const [hasBasement, setHasBasement] = useState(false);
  
  const [hasGarbageChute, setHasGarbageChute] = useState(false);
  const [publicPremisesCount, setPublicPremisesCount] = useState('');
  const [totalPublicArea, setTotalPublicArea] = useState('');
  const [hasQuartergraphy, setHasQuartergraphy] = useState(false);
  const [totalApartmentArea, setTotalApartmentArea] = useState('');
  const [oneRoomCount, setOneRoomCount] = useState('');
  const [twoRoomCount, setTwoRoomCount] = useState('');
  const [threeRoomCount, setThreeRoomCount] = useState('');
  const [fourRoomCount, setFourRoomCount] = useState('');
  const [moreThanFourRoomCount, setMoreThanFourRoomCount] = useState('');
  const [penthouseCount, setPenthouseCount] = useState('');
  const [studioCount, setStudioCount] = useState('');
  const [hasExploitedRoof, setHasExploitedRoof] = useState(false);
  const [publicPremisesPurpose, setPublicPremisesPurpose] = useState<string[] | null>(null);
  
  // Состояния для стилобатов
  const [stilobatCalculated, setStilobatCalculated] = useState<boolean[]>([]);
  const [stilobatFloors, setStilobatFloors] = useState<string[]>([]);
  const [stilobatAvgArea, setStilobatAvgArea] = useState<string[]>([]);
  const [stilobatAvgHeight, setStilobatAvgHeight] = useState<string[]>([]);
  const [stilobatTotalArea, setStilobatTotalArea] = useState<string[]>([]);
  const [stilobatGnsArea, setStilobatGnsArea] = useState<string[]>([]);
  const [stilobatVolume, setStilobatVolume] = useState<string[]>([]);
  const [stilobatStairs, setStilobatStairs] = useState<string[]>([]);
  const [stilobatSmokelessStairs, setStilobatSmokelessStairs] = useState<string[]>([]);
  const [stilobatLifts, setStilobatLifts] = useState<string[]>([]);
  
  // Состояния для пристроек
  const [annexCalculated, setAnnexCalculated] = useState<boolean[]>([]);
  const [annexFloors, setAnnexFloors] = useState<string[]>([]);
  const [annexArea, setAnnexArea] = useState<string[]>([]);
  const [annexHeight, setAnnexHeight] = useState<string[]>([]);
  const [annexTotalArea, setAnnexTotalArea] = useState<string[]>([]);
  const [annexGnsArea, setAnnexGnsArea] = useState<string[]>([]);
  const [annexVolume, setAnnexVolume] = useState<string[]>([]);
  const [annexStairs, setAnnexStairs] = useState<string[]>([]);
  const [annexSmokelessStairs, setAnnexSmokelessStairs] = useState<string[]>([]);
  const [annexLifts, setAnnexLifts] = useState<string[]>([]);
  
  // Состояния для корпусов и секций
  const [sectionsCounts, setSectionsCounts] = useState<number[]>([]);
  const [sectionCalculated, setSectionCalculated] = useState<boolean[][]>([]);
  const [sectionAreas, setSectionAreas] = useState<string[][]>([]);
  const [sectionFloors, setSectionFloors] = useState<string[][]>([]);
  const [sectionFirstFloorHeight, setSectionFirstFloorHeight] = useState<string[][]>([]);
  const [sectionTypicalFloorHeight, setSectionTypicalFloorHeight] = useState<string[][]>([]);
  const [sectionTotalArea, setSectionTotalArea] = useState<string[][]>([]);
  const [sectionGnsArea, setSectionGnsArea] = useState<string[][]>([]);
  const [sectionVolume, setSectionVolume] = useState<string[][]>([]);
  const [sectionFireHeight, setSectionFireHeight] = useState<string[][]>([]);
  const [sectionStaircases, setSectionStaircases] = useState<string[][]>([]);
  const [sectionSmokelessStaircases, setSectionSmokelessStaircases] = useState<string[][]>([]);
  const [sectionElevators, setSectionElevators] = useState<string[][]>([]);
  
  // Состояния для подземной части
  const [undergroundCalculated, setUndergroundCalculated] = useState(false);
  const [undergroundFloors, setUndergroundFloors] = useState('');
  const [undergroundAvgArea, setUndergroundAvgArea] = useState('');
  const [undergroundAvgHeight, setUndergroundAvgHeight] = useState('');
  const [undergroundStorageArea, setUndergroundStorageArea] = useState('');
  const [undergroundTotalArea, setUndergroundTotalArea] = useState('');
  const [hasUndergroundParking, setHasUndergroundParking] = useState(false);
  
  // Состояния для расчетных данных
  const [objectCalculated, setObjectCalculated] = useState(false);
  const [calculatedStairs, setCalculatedStairs] = useState('');
  const [calculatedElevators, setCalculatedElevators] = useState('');
  const [calculatedStaircases, setCalculatedStaircases] = useState('');
  const [calculatedPublicArea, setCalculatedPublicArea] = useState('');
  const [calculatedPublicPurpose, setCalculatedPublicPurpose] = useState('');
  const [calculatedPublicCount, setCalculatedPublicCount] = useState('');
  const [calculatedAbovegroundVolume, setCalculatedAbovegroundVolume] = useState('');
  const [calculatedResidents, setCalculatedResidents] = useState('');
  const [calculatedUndergroundVolume, setCalculatedUndergroundVolume] = useState('');
  const [calculatedTotalArea, setCalculatedTotalArea] = useState('');
  const [calculatedTotalVolume, setCalculatedTotalVolume] = useState('');
  const [calculatedResidentsCount, setCalculatedResidentsCount] = useState('');

  // Состояния для подземной части
  const [undergroundGnsArea, setUndergroundGnsArea] = useState('');
  const [undergroundVolume, setUndergroundVolume] = useState('');
  const [undergroundStairs, setUndergroundStairs] = useState('');
  const [undergroundSmokelessStairs, setUndergroundSmokelessStairs] = useState('');
  const [parkingFloors, setParkingFloors] = useState('');
  const [parkingTiers, setParkingTiers] = useState('');
  const [parkingTotalArea, setParkingTotalArea] = useState('');
  const [parkingFireCompartments, setParkingFireCompartments] = useState('');
  const [parkingSpaces, setParkingSpaces] = useState('');
  const [hasCarWash, setHasCarWash] = useState(false);

  // Инициализация массивов при изменении количества пристроек
  useEffect(() => {
    if (!isHydrated.current) {
      return;
    }
    setAnnexCalculated(Array(annexCount).fill(false));
    setAnnexFloors(Array(annexCount).fill(''));
    setAnnexArea(Array(annexCount).fill(''));
    setAnnexHeight(Array(annexCount).fill(''));
    setAnnexTotalArea(Array(annexCount).fill(''));
    setAnnexGnsArea(Array(annexCount).fill(''));
    setAnnexVolume(Array(annexCount).fill(''));
    setAnnexStairs(Array(annexCount).fill(''));
    setAnnexSmokelessStairs(Array(annexCount).fill(''));
    setAnnexLifts(Array(annexCount).fill(''));
  }, [annexCount]);

  // Инициализация массивов при изменении количества стилобатов
  useEffect(() => {
    if (!isHydrated.current) {
      return;
    }
    setStilobatCalculated(Array(stilobatCount).fill(false));
    setStilobatFloors(Array(stilobatCount).fill(''));
    setStilobatAvgArea(Array(stilobatCount).fill(''));
    setStilobatAvgHeight(Array(stilobatCount).fill(''));
    setStilobatTotalArea(Array(stilobatCount).fill(''));
    setStilobatGnsArea(Array(stilobatCount).fill(''));
    setStilobatVolume(Array(stilobatCount).fill(''));
    setStilobatStairs(Array(stilobatCount).fill(''));
    setStilobatSmokelessStairs(Array(stilobatCount).fill(''));
    setStilobatLifts(Array(stilobatCount).fill(''));
  }, [stilobatCount]);

  useEffect(() => {
    if (!isHydrated.current) {
      return;
    }
    const newSectionsCounts = Array(buildingCount).fill(0);
    const newSectionCalculated = Array(buildingCount).fill([]).map(() => []);
    const newSectionAreas = Array(buildingCount).fill([]).map(() => []);
    const newSectionFloors = Array(buildingCount).fill([]).map(() => []);
    const newSectionFirstFloorHeight = Array(buildingCount).fill([]).map(() => []);
    const newSectionTypicalFloorHeight = Array(buildingCount).fill([]).map(() => []);
    const newSectionTotalArea = Array(buildingCount).fill([]).map(() => []);
    const newSectionGnsArea = Array(buildingCount).fill([]).map(() => []);
    const newSectionVolume = Array(buildingCount).fill([]).map(() => []);
    const newSectionFireHeight = Array(buildingCount).fill([]).map(() => []);
    const newSectionStaircases = Array(buildingCount).fill([]).map(() => []);
    const newSectionSmokelessStaircases = Array(buildingCount).fill([]).map(() => []);
    const newSectionElevators = Array(buildingCount).fill([]).map(() => []);
    
    setSectionsCounts(newSectionsCounts);
    setSectionCalculated(newSectionCalculated);
    setSectionAreas(newSectionAreas);
    setSectionFloors(newSectionFloors);
    setSectionFirstFloorHeight(newSectionFirstFloorHeight);
    setSectionTypicalFloorHeight(newSectionTypicalFloorHeight);
    setSectionTotalArea(newSectionTotalArea);
    setSectionGnsArea(newSectionGnsArea);
    setSectionVolume(newSectionVolume);
    setSectionFireHeight(newSectionFireHeight);
    setSectionStaircases(newSectionStaircases);
    setSectionSmokelessStaircases(newSectionSmokelessStaircases);
    setSectionElevators(newSectionElevators);
  }, [buildingCount]);

  useEffect(() => {
    if (isHydrated.current) {
      return;
    }

    setAreaValue(data.areaValue ?? '');
    setUndergroundParkingIndex(data.undergroundParkingIndex ?? null);
    setStilobatLinkedIndex(data.stilobatLinkedIndex ?? null);
    setAnnexLinkedIndex(data.annexLinkedIndex ?? null);
    
    setBuildingCount(data.buildingCount ?? 0);
    setStilobatCount(data.stilobatCount ?? 0);
    setAnnexCount(data.annexCount ?? 0);
    setHasTechFloor(Boolean(data.hasTechFloor));
    setHasTechAttic(Boolean(data.hasTechAttic));
    setHasBasement(Boolean(data.hasBasement));

    setHasGarbageChute(Boolean(data.hasGarbageChute));
    setPublicPremisesCount(data.publicPremisesCount ?? '');
    setTotalPublicArea(data.totalPublicArea ?? '');
    setHasQuartergraphy(Boolean(data.hasQuartergraphy));
    setTotalApartmentArea(data.totalApartmentArea ?? '');
    setOneRoomCount(data.oneRoomCount ?? '');
    setTwoRoomCount(data.twoRoomCount ?? '');
    setThreeRoomCount(data.threeRoomCount ?? '');
    setFourRoomCount(data.fourRoomCount ?? '');
    setMoreThanFourRoomCount(data.moreThanFourRoomCount ?? '');
    setPenthouseCount(data.penthouseCount ?? '');
    setStudioCount(data.studioCount ?? '');
    setHasExploitedRoof(Boolean(data.hasExploitedRoof));
    setPublicPremisesPurpose(data.publicPremisesPurpose ?? null);

    setStilobatCalculated(Array.isArray(data.stilobatCalculated) ? [...data.stilobatCalculated] : []);
    setStilobatFloors(Array.isArray(data.stilobatFloors) ? [...data.stilobatFloors] : []);
    setStilobatAvgArea(Array.isArray(data.stilobatAvgArea) ? [...data.stilobatAvgArea] : []);
    setStilobatAvgHeight(Array.isArray(data.stilobatAvgHeight) ? [...data.stilobatAvgHeight] : []);
    setStilobatTotalArea(Array.isArray(data.stilobatTotalArea) ? [...data.stilobatTotalArea] : []);
    setStilobatGnsArea(Array.isArray(data.stilobatGnsArea) ? [...data.stilobatGnsArea] : []);
    setStilobatVolume(Array.isArray(data.stilobatVolume) ? [...data.stilobatVolume] : []);
    setStilobatStairs(Array.isArray(data.stilobatStairs) ? [...data.stilobatStairs] : []);
    setStilobatSmokelessStairs(Array.isArray(data.stilobatSmokelessStairs) ? [...data.stilobatSmokelessStairs] : []);
    setStilobatLifts(Array.isArray(data.stilobatLifts) ? [...data.stilobatLifts] : []);

    setAnnexCalculated(Array.isArray(data.annexCalculated) ? [...data.annexCalculated] : []);
    setAnnexFloors(Array.isArray(data.annexFloors) ? [...data.annexFloors] : []);
    setAnnexArea(Array.isArray(data.annexArea) ? [...data.annexArea] : []);
    setAnnexHeight(Array.isArray(data.annexHeight) ? [...data.annexHeight] : []);
    setAnnexTotalArea(Array.isArray(data.annexTotalArea) ? [...data.annexTotalArea] : []);
    setAnnexGnsArea(Array.isArray(data.annexGnsArea) ? [...data.annexGnsArea] : []);
    setAnnexVolume(Array.isArray(data.annexVolume) ? [...data.annexVolume] : []);
    setAnnexStairs(Array.isArray(data.annexStairs) ? [...data.annexStairs] : []);
    setAnnexSmokelessStairs(Array.isArray(data.annexSmokelessStairs) ? [...data.annexSmokelessStairs] : []);
    setAnnexLifts(Array.isArray(data.annexLifts) ? [...data.annexLifts] : []);

    setSectionsCounts(Array.isArray(data.sectionsCounts) ? [...data.sectionsCounts] : []);
    setSectionCalculated(
      Array.isArray(data.sectionCalculated)
        ? data.sectionCalculated.map((row) => (Array.isArray(row) ? [...row] : []))
        : [],
    );
    setSectionAreas(
      Array.isArray(data.sectionAreas)
        ? data.sectionAreas.map((row) => (Array.isArray(row) ? [...row] : []))
        : [],
    );
    setSectionFloors(
      Array.isArray(data.sectionFloors)
        ? data.sectionFloors.map((row) => (Array.isArray(row) ? [...row] : []))
        : [],
    );
    setSectionFirstFloorHeight(
      Array.isArray(data.sectionFirstFloorHeight)
        ? data.sectionFirstFloorHeight.map((row) => (Array.isArray(row) ? [...row] : []))
        : [],
    );
    setSectionTypicalFloorHeight(
      Array.isArray(data.sectionTypicalFloorHeight)
        ? data.sectionTypicalFloorHeight.map((row) => (Array.isArray(row) ? [...row] : []))
        : [],
    );
    setSectionTotalArea(
      Array.isArray(data.sectionTotalArea)
        ? data.sectionTotalArea.map((row) => (Array.isArray(row) ? [...row] : []))
        : [],
    );
    setSectionGnsArea(
      Array.isArray(data.sectionGnsArea)
        ? data.sectionGnsArea.map((row) => (Array.isArray(row) ? [...row] : []))
        : [],
    );
    setSectionVolume(
      Array.isArray(data.sectionVolume)
        ? data.sectionVolume.map((row) => (Array.isArray(row) ? [...row] : []))
        : [],
    );
    setSectionFireHeight(
      Array.isArray(data.sectionFireHeight)
        ? data.sectionFireHeight.map((row) => (Array.isArray(row) ? [...row] : []))
        : [],
    );
    setSectionStaircases(
      Array.isArray(data.sectionStaircases)
        ? data.sectionStaircases.map((row) => (Array.isArray(row) ? [...row] : []))
        : [],
    );
    setSectionSmokelessStaircases(
      Array.isArray(data.sectionSmokelessStaircases)
        ? data.sectionSmokelessStaircases.map((row) => (Array.isArray(row) ? [...row] : []))
        : [],
    );
    setSectionElevators(
      Array.isArray(data.sectionElevators)
        ? data.sectionElevators.map((row) => (Array.isArray(row) ? [...row] : []))
        : [],
    );

    setUndergroundCalculated(Boolean(data.undergroundCalculated));
    setUndergroundFloors(data.undergroundFloors ?? '');
    setUndergroundAvgArea(data.undergroundAvgArea ?? '');
    setUndergroundAvgHeight(data.undergroundAvgHeight ?? '');
    setUndergroundStorageArea(data.undergroundStorageArea ?? '');
    setUndergroundTotalArea(data.undergroundTotalArea ?? '');
    setHasUndergroundParking(Boolean(data.hasUndergroundParking));

    setObjectCalculated(Boolean(data.objectCalculated));
    setCalculatedStairs(data.calculatedStairs ?? '');
    setCalculatedElevators(data.calculatedElevators ?? '');
    setCalculatedStaircases(data.calculatedStaircases ?? '');
    setCalculatedPublicArea(data.calculatedPublicArea ?? '');
    setCalculatedPublicPurpose(data.calculatedPublicPurpose ?? '');
    setCalculatedPublicCount(data.calculatedPublicCount ?? '');
    setCalculatedAbovegroundVolume(data.calculatedAbovegroundVolume ?? '');
    setCalculatedResidents(data.calculatedResidents ?? '');
    setCalculatedUndergroundVolume(data.calculatedUndergroundVolume ?? '');
    setCalculatedTotalArea(data.calculatedTotalArea ?? '');
    setCalculatedTotalVolume(data.calculatedTotalVolume ?? '');
    setCalculatedResidentsCount(data.calculatedResidentsCount ?? '');

    isHydrated.current = true;
  }, [data]);

  useEffect(() => {
    if (!isHydrated.current) {
      return;
    }

    const payload: ArchitectureFormData = {
      areaValue,
      undergroundParkingIndex,
      stilobatLinkedIndex,
      annexLinkedIndex,
      buildingCount,
      stilobatCount,
      annexCount,
      hasTechFloor,
      hasTechAttic,
      hasBasement,
      hasGarbageChute,
      publicPremisesCount,
      totalPublicArea,
      hasQuartergraphy,
      totalApartmentArea,
      oneRoomCount,
      twoRoomCount,
      threeRoomCount,
      fourRoomCount,
      moreThanFourRoomCount,
      penthouseCount,
      studioCount,
      hasExploitedRoof,
      publicPremisesPurpose,
      stilobatCalculated,
      stilobatFloors,
      stilobatAvgArea,
      stilobatAvgHeight,
      stilobatTotalArea,
      stilobatGnsArea,
      stilobatVolume,
      stilobatStairs,
      stilobatSmokelessStairs,
      stilobatLifts,
      annexCalculated,
      annexFloors,
      annexArea,
      annexHeight,
      annexTotalArea,
      annexGnsArea,
      annexVolume,
      annexStairs,
      annexSmokelessStairs,
      annexLifts,
      sectionsCounts,
      sectionCalculated,
      sectionAreas,
      sectionFloors,
      sectionFirstFloorHeight,
      sectionTypicalFloorHeight,
      sectionTotalArea,
      sectionGnsArea,
      sectionVolume,
      sectionFireHeight,
      sectionStaircases,
      sectionSmokelessStaircases,
      sectionElevators,
      undergroundCalculated,
      undergroundFloors,
      undergroundAvgArea,
      undergroundAvgHeight,
      undergroundStorageArea,
      undergroundTotalArea,
      hasUndergroundParking,
      objectCalculated,
      calculatedStairs,
      calculatedElevators,
      calculatedStaircases,
      calculatedPublicArea,
      calculatedPublicPurpose,
      calculatedPublicCount,
      calculatedAbovegroundVolume,
      calculatedResidents,
      calculatedUndergroundVolume,
      calculatedTotalArea,
      calculatedTotalVolume,
      calculatedResidentsCount,
      undergroundGnsArea: '',
      undergroundVolume: '',
      undergroundStairs: '',
      undergroundSmokelessStairs: '',
      parkingFloors: '',
      parkingTiers: '',
      parkingTotalArea: '',
      parkingFireCompartments: '',
      parkingSpaces: '',
      hasCarWash: false
    };

    setData(payload);
  }, [
    areaValue,
    undergroundParkingIndex,
    stilobatLinkedIndex,
    annexLinkedIndex,
    buildingCount,
    stilobatCount,
    annexCount,
    hasTechFloor,
    hasTechAttic,
    hasBasement,
    hasGarbageChute,
    publicPremisesCount,
    totalPublicArea,
    hasQuartergraphy,
    totalApartmentArea,
    oneRoomCount,
    twoRoomCount,
    threeRoomCount,
    fourRoomCount,
    moreThanFourRoomCount,
    penthouseCount,
    studioCount,
    hasExploitedRoof,
    publicPremisesPurpose,
    stilobatCalculated,
    stilobatFloors,
    stilobatAvgArea,
    stilobatAvgHeight,
    stilobatTotalArea,
    stilobatGnsArea,
    stilobatVolume,
    stilobatStairs,
    stilobatSmokelessStairs,
    stilobatLifts,
    annexCalculated,
    annexFloors,
    annexArea,
    annexHeight,
    annexTotalArea,
    annexGnsArea,
    annexVolume,
    annexStairs,
    annexSmokelessStairs,
    annexLifts,
    sectionsCounts,
    sectionCalculated,
    sectionAreas,
    sectionFloors,
    sectionFirstFloorHeight,
    sectionTypicalFloorHeight,
    sectionTotalArea,
    sectionGnsArea,
    sectionVolume,
    sectionFireHeight,
    sectionStaircases,
    sectionSmokelessStaircases,
    sectionElevators,
    undergroundCalculated,
    undergroundFloors,
    undergroundAvgArea,
    undergroundAvgHeight,
    undergroundStorageArea,
    undergroundTotalArea,
    hasUndergroundParking,
    objectCalculated,
    calculatedStairs,
    calculatedElevators,
    calculatedStaircases,
    calculatedPublicArea,
    calculatedPublicPurpose,
    calculatedPublicCount,
    calculatedAbovegroundVolume,
    calculatedResidents,
    calculatedUndergroundVolume,
    calculatedTotalArea,
    calculatedTotalVolume,
    calculatedResidentsCount,
    setData,
  ]);

  const handleAreaChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setAreaValue(e.target.value);
  };

  const handleUndergroundParkingChange = (value: string[] | null) => {
    setUndergroundParkingIndex(value);
  };

  const handleStilobatLinkedChange = (value: string[] | null) => {
    setStilobatLinkedIndex(value);
  };

  const handleAnnexLinkedChange = (value: string[] | null) => {
    setAnnexLinkedIndex(value);
  };

  const handleBuildingCountChange = (value: number) => {
    setBuildingCount(value);
  };

  const handleSectionCountChange = (index: number, value: number) => {
    const newSectionsCounts = [...sectionsCounts];
    newSectionsCounts[index] = value;
    setSectionsCounts(newSectionsCounts);
    
    const newSectionAreas = [...sectionAreas];
    newSectionAreas[index] = Array(value).fill('');
    setSectionAreas(newSectionAreas);
    
    const newSectionCalculated = [...sectionCalculated];
    newSectionCalculated[index] = Array(value).fill(false);
    setSectionCalculated(newSectionCalculated);

    const newSectionFloors = [...sectionFloors];
    newSectionFloors[index] = Array(value).fill('');
    setSectionFloors(newSectionFloors);

    const newSectionFirstFloorHeight = [...sectionFirstFloorHeight];
    newSectionFirstFloorHeight[index] = Array(value).fill('');
    setSectionFirstFloorHeight(newSectionFirstFloorHeight);

    const newSectionTypicalFloorHeight = [...sectionTypicalFloorHeight];
    newSectionTypicalFloorHeight[index] = Array(value).fill('');
    setSectionTypicalFloorHeight(newSectionTypicalFloorHeight);

    const newSectionTotalArea = [...sectionTotalArea];
    newSectionTotalArea[index] = Array(value).fill('');
    setSectionTotalArea(newSectionTotalArea);

    const newSectionGnsArea = [...sectionGnsArea];
    newSectionGnsArea[index] = Array(value).fill('');
    setSectionGnsArea(newSectionGnsArea);

    const newSectionVolume = [...sectionVolume];
    newSectionVolume[index] = Array(value).fill('');
    setSectionVolume(newSectionVolume);

    const newSectionFireHeight = [...sectionFireHeight];
    newSectionFireHeight[index] = Array(value).fill('');
    setSectionFireHeight(newSectionFireHeight);

    const newSectionStaircases = [...sectionStaircases];
    newSectionStaircases[index] = Array(value).fill('');
    setSectionStaircases(newSectionStaircases);

    const newSectionSmokelessStaircases = [...sectionSmokelessStaircases];
    newSectionSmokelessStaircases[index] = Array(value).fill('');
    setSectionSmokelessStaircases(newSectionSmokelessStaircases);

    const newSectionElevators = [...sectionElevators];
    newSectionElevators[index] = Array(value).fill('');
    setSectionElevators(newSectionElevators);
  };

  // Обработчики для общих полей
  // const onHasGarbageChuteChange = (value: boolean) => {
  //   setHasGarbageChute(value);
  // };

  const onPublicPremisesCountChange = (value: string) => {
    setPublicPremisesCount(value);
  };

  const onPublicPremisesPurposeChange = (value: string[] | null) => {
    setPublicPremisesPurpose(value);
  };

  const materialOptionsA = [
    { value: '1', label: '1' },
    { value: '2', label: '2' },
    { value: '3', label: '3' },
    { value: '4', label: '4' },
    { value: '5', label: '5' },
    { value: '6', label: '6' },
    { value: '7', label: '7' },
    { value: '8', label: '8' },
    { value: '9', label: '9' },
    { value: '10', label: '10' },
    { value: '11', label: '11' },
    { value: '12', label: '12' },
  ];

  // Обработчики для отдельных полей пристроек
  const handleAnnexCalculatedChange = (index: number, checked: boolean) => {
    const newCalculated = [...annexCalculated];
    newCalculated[index] = checked;
    setAnnexCalculated(newCalculated);
  };

  const handleAnnexFloorsChange = (index: number, value: string) => {
    const newFloors = [...annexFloors];
    newFloors[index] = value;
    setAnnexFloors(newFloors);
  };

  const handleAnnexAreaChange = (index: number, value: string) => {
    const newArea = [...annexArea];
    newArea[index] = value;
    setAnnexArea(newArea);
  };

  const handleAnnexHeightChange = (index: number, value: string) => {
    const newHeight = [...annexHeight];
    newHeight[index] = value;
    setAnnexHeight(newHeight);
  };

  const handleAnnexTotalAreaChange = (index: number, value: string) => {
    const newTotalArea = [...annexTotalArea];
    newTotalArea[index] = value;
    setAnnexTotalArea(newTotalArea);
  };

  const handleAnnexGnsAreaChange = (index: number, value: string) => {
    const newGnsArea = [...annexGnsArea];
    newGnsArea[index] = value;
    setAnnexGnsArea(newGnsArea);
  };

  const handleAnnexVolumeChange = (index: number, value: string) => {
    const newVolume = [...annexVolume];
    newVolume[index] = value;
    setAnnexVolume(newVolume);
  };

  const handleAnnexStairsChange = (index: number, value: string) => {
    const newStairs = [...annexStairs];
    newStairs[index] = value;
    setAnnexStairs(newStairs);
  };

  const handleAnnexSmokelessStairsChange = (index: number, value: string) => {
    const newSmokelessStairs = [...annexSmokelessStairs];
    newSmokelessStairs[index] = value;
    setAnnexSmokelessStairs(newSmokelessStairs);
  };

  const handleAnnexLiftsChange = (index: number, value: string) => {
    const newLifts = [...annexLifts];
    newLifts[index] = value;
    setAnnexLifts(newLifts);
  };

  const renderAnnexes = () => {
    const elements = [];
    for (let i = 0; i < annexCount; i++) {
      elements.push(
        <div key={`annex-container-${i}`} className={styles.annexContainer}>
          <h2 style={{ fontFamily: 'Montserrat', textAlign: 'left' }}>
            Пристройка {i + 1}
          </h2>
          <CheckboxTrue 
            key={`annex-calculated-${i}`}
            checked={annexCalculated[i] || false}
            onChange={(checked) => handleAnnexCalculatedChange(i, checked)}
            label="Расчетные данные"
          />
          <NumberField 
            key={`annex-floors-${i}`}
            title="Количество этажей"
            value={annexFloors[i] || ''}
            onChange={(value) => handleAnnexFloorsChange(i, value)}
            placeholder="1"
          />
          <NumberField 
            key={`annex-area-${i}`}
            title="Площадь этажа в м²"
            value={annexArea[i] || ''}
            placeholder='1'
            onChange={(value) => handleAnnexAreaChange(i, value)}
          />
          <NumberField 
            key={`annex-height-${i}`}
            title="Средняя высота этажа в м"
            value={annexHeight[i] || ''}
            placeholder='1'
            onChange={(value) => handleAnnexHeightChange(i, value)}
          />
          <NumberField 
            key={`annex-total-area-${i}`}
            title="Общая площадь в м²"
            value={annexTotalArea[i] || ''}
            placeholder='1'
            onChange={(value) => handleAnnexTotalAreaChange(i, value)}
            disabled
          />
          <NumberField 
            key={`annex-gns-area-${i}`}
            title="Площадь ГНС в м²"
            value={annexGnsArea[i] || ''}
            placeholder='1'
            onChange={(value) => handleAnnexGnsAreaChange(i, value)}
            disabled
          />
          <NumberField 
            key={`annex-volume-${i}`}
            title="Строительный объем в м³"
            value={annexVolume[i] || ''}
            placeholder='1'
            onChange={(value) => handleAnnexVolumeChange(i, value)}
            disabled
          />
          <NumberField 
            key={`annex-stairs-${i}`}
            title="Количество лестничных клеток"
            value={annexStairs[i] || ''}
            placeholder='1'
            onChange={(value) => handleAnnexStairsChange(i, value)}
            disabled
          />
          <NumberField 
            key={`annex-smokeless-stairs-${i}`}
            title="Количество незадымляемых лестничных клеток"
            value={annexSmokelessStairs[i] || ''}
            placeholder='1'
            onChange={(value) => handleAnnexSmokelessStairsChange(i, value)}
            disabled
          />
          <NumberField 
            key={`annex-lifts-${i}`}
            title="Количество лифтов"
            value={annexLifts[i] || ''}
            placeholder='1'
            onChange={(value) => handleAnnexLiftsChange(i, value)}
            disabled
          />
        </div>
      );
      
      if (annexCount % 2 !== 0 && i === annexCount - 1) {
        elements.push(<div key={`annex-empty-${i}`}></div>);
      }
    }

    elements.push(
      <div key="final-stillobat-question" className={styles.finalCorpusQuestion} style={{ gridColumn: 'span 2' }}>
        <div className={styles.leftPart}>
          <div key="public-premises-count">
            <h2 style={{ fontFamily: 'Montserrat', textAlign: 'left', fontSize: '20px', marginBlockStart: 0 }}>Количество общественных помещений</h2>
            <Input 
              type="number" 
              placeholder="Например: 2" 
              className={styles.inputFieldClassic}
              value={publicPremisesCount}
              onChange={(e: { target: { value: string; }; }) => onPublicPremisesCountChange(e.target.value)}
            />
          </div>
        </div>

        <div className={styles.rightPart}>
          <Select
            key="public-premises-purpose"
            title="Назначение общественных помещений"
            options={[]}
            value={publicPremisesPurpose}
            onChange={onPublicPremisesPurposeChange}
            placeholder="Выберите нужное значение"
            multiple
          />
        </div>
      </div>
    );

    return elements;
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Основные архитектурные решения</h1>
      <div className={styles.inputContainer}>
        <h2 style={{ fontFamily: 'Montserrat' }}>Площадь застройки в м²</h2>
        <Input 
          type="number" 
          placeholder="Например: 11303,0" 
          className={styles.inputFieldClassic}
          value={areaValue}
          onChange={handleAreaChange}
        />
      </div>

      <div className={styles.gridContainer}>
        <div className={styles.inputContainer}>
          <h2 style={{ fontFamily: 'Montserrat' }}>Количество корпусов в объекте капитального строительства</h2>
          <Input 
            type="number" 
            placeholder="Например: 2" 
            className={styles.inputFieldClassic}
            value={String(buildingCount)}
            onChange={(e) => handleBuildingCountChange(parseInt(e.target.value) || 0)}
          />
        </div>
        <Select 
          title='Корпуса, расположенные на подземной автостоянке'
          options={materialOptionsA}
          value={undergroundParkingIndex}
          onChange={handleUndergroundParkingChange}
          placeholder="Выберите нужное значение"
          multiple={true}
          inlineOptions={true}
        />
        <div className={styles.inputContainer}>
          <h2 style={{ fontFamily: 'Montserrat' }}>Количество стилобатов</h2>
          <Input 
            type="number" 
            placeholder="Например: 2" 
            className={styles.inputFieldClassic}
            value={String(stilobatCount)}
            onChange={(e) => setStilobatCount(parseInt(e.target.value) || 0)}
          />
        </div>
        <Select 
          title='Корпуса, связанные с стилобатом'
          options={materialOptionsA}
          value={stilobatLinkedIndex}
          onChange={handleStilobatLinkedChange}
          placeholder="Выберите нужное значение"
          multiple={true}
          inlineOptions={true}
        />
        <div className={styles.inputContainer}>
          <h2 style={{ fontFamily: 'Montserrat' }}>Количество пристроенных помещений</h2>
          <Input 
            type="number" 
            placeholder="Например: 1" 
            className={styles.inputFieldClassic}
            value={String(annexCount)}
            onChange={(e) => setAnnexCount(parseInt(e.target.value) || 0)}
          />
        </div>
        <Select 
          title='Корпуса, связанные с пристроенными помещениями'
          options={materialOptionsA}
          value={annexLinkedIndex}
          onChange={handleAnnexLinkedChange}
          placeholder="Выберите нужное значение"
          multiple={true}
          inlineOptions={true}
        />
      </div>

      <NumberFieldsGrid title="Стилобатная часть">
        <Stilobaty
          stilobatCount={stilobatCount}
          stilobatCalculated={stilobatCalculated}
          stilobatFloors={stilobatFloors}
          stilobatAvgArea={stilobatAvgArea}
          stilobatAvgHeight={stilobatAvgHeight}
          stilobatTotalArea={stilobatTotalArea}
          stilobatGnsArea={stilobatGnsArea}
          stilobatVolume={stilobatVolume}
          stilobatStairs={stilobatStairs}
          stilobatSmokelessStairs={stilobatSmokelessStairs}
          stilobatLifts={stilobatLifts}
          hasGarbageChute={hasGarbageChute}
          publicPremisesCount={publicPremisesCount}
          publicPremisesPurpose={publicPremisesPurpose}
          onStilobatCalculatedChange={setStilobatCalculated}
          onStilobatFloorsChange={setStilobatFloors}
          onStilobatAvgAreaChange={setStilobatAvgArea}
          onStilobatAvgHeightChange={setStilobatAvgHeight}
          onStilobatTotalAreaChange={setStilobatTotalArea}
          onStilobatGnsAreaChange={setStilobatGnsArea}
          onStilobatVolumeChange={setStilobatVolume}
          onStilobatStairsChange={setStilobatStairs}
          onStilobatSmokelessStairsChange={setStilobatSmokelessStairs}
          onStilobatLiftsChange={setStilobatLifts}
          onHasGarbageChuteChange={setHasGarbageChute}
          onPublicPremisesCountChange={setPublicPremisesCount}
          onPublicPremisesPurposeChange={setPublicPremisesPurpose}
        />
      </NumberFieldsGrid>

      <NumberFieldsGrid title="Пристроенные помещения общественного назначения">
        {renderAnnexes()}
      </NumberFieldsGrid>

      <NumberFieldsGrid title="Наземная часть корпусов">
        <Buildings
          buildingCount={buildingCount}
          sectionsCounts={sectionsCounts}
          sectionCalculated={sectionCalculated}
          sectionAreas={sectionAreas}
          sectionFloors={sectionFloors}
          sectionFirstFloorHeight={sectionFirstFloorHeight}
          sectionTypicalFloorHeight={sectionTypicalFloorHeight}
          sectionTotalArea={sectionTotalArea}
          sectionGnsArea={sectionGnsArea}
          sectionVolume={sectionVolume}
          sectionFireHeight={sectionFireHeight}
          sectionStaircases={sectionStaircases}
          sectionSmokelessStaircases={sectionSmokelessStaircases}
          sectionElevators={sectionElevators}
          hasTechFloor={hasTechFloor}
          hasBasement={hasBasement}
          hasTechAttic={hasTechAttic}
          hasGarbageChute={hasGarbageChute}
          publicPremisesCount={publicPremisesCount}
          totalPublicArea={totalPublicArea}
          hasQuartergraphy={hasQuartergraphy}
          totalApartmentArea={totalApartmentArea}
          oneRoomCount={oneRoomCount}
          twoRoomCount={twoRoomCount}
          threeRoomCount={threeRoomCount}
          fourRoomCount={fourRoomCount}
          moreThanFourRoomCount={moreThanFourRoomCount}
          penthouseCount={penthouseCount}
          studioCount={studioCount}
          hasExploitedRoof={hasExploitedRoof}
          publicPremisesPurpose={publicPremisesPurpose}
          onSectionCountChange={handleSectionCountChange}
          onSectionCalculatedChange={setSectionCalculated}
          onSectionAreasChange={setSectionAreas}
          onSectionFloorsChange={setSectionFloors}
          onSectionFirstFloorHeightChange={setSectionFirstFloorHeight}
          onSectionTypicalFloorHeightChange={setSectionTypicalFloorHeight}
          onSectionTotalAreaChange={setSectionTotalArea}
          onSectionGnsAreaChange={setSectionGnsArea}
          onSectionVolumeChange={setSectionVolume}
          onSectionFireHeightChange={setSectionFireHeight}
          onSectionStaircasesChange={setSectionStaircases}
          onSectionSmokelessStaircasesChange={setSectionSmokelessStaircases}
          onSectionElevatorsChange={setSectionElevators}
          onHasTechFloorChange={setHasTechFloor}
          onHasBasementChange={setHasBasement}
          onHasTechAtticChange={setHasTechAttic}
          onHasGarbageChuteChange={setHasGarbageChute}
          onPublicPremisesCountChange={setPublicPremisesCount}
          onTotalPublicAreaChange={setTotalPublicArea}
          onHasQuartergraphyChange={setHasQuartergraphy}
          onTotalApartmentAreaChange={setTotalApartmentArea}
          onOneRoomCountChange={setOneRoomCount}
          onTwoRoomCountChange={setTwoRoomCount}
          onThreeRoomCountChange={setThreeRoomCount}
          onFourRoomCountChange={setFourRoomCount}
          onMoreThanFourRoomCountChange={setMoreThanFourRoomCount}
          onPenthouseCountChange={setPenthouseCount}
          onStudioCountChange={setStudioCount}
          onHasExploitedRoofChange={setHasExploitedRoof}
          onPublicPremisesPurposeChange={setPublicPremisesPurpose}
        />
      </NumberFieldsGrid>

      <NumberFieldsGrid title="Подземная часть корпусов">
        <CheckboxTrue 
          key="underground-calculated"
          checked={undergroundCalculated}
          onChange={setUndergroundCalculated}
          label="Расчетные данные"
        />
        
        <NumberField 
          key="underground-floors"
          title="Количество этажей"
          value={undergroundFloors}
          onChange={setUndergroundFloors}
          placeholder="1"
        />

        <NumberField 
          key="underground-avg-area"
          title="Средняя площадь этажа в м²"
          value={undergroundAvgArea}
          placeholder='1'
          onChange={setUndergroundAvgArea}
        />

        <NumberField 
          key="underground-avg-height"
          title="Средняя высота этажа в м"
          value={undergroundAvgHeight}
          placeholder='1'
          onChange={setUndergroundAvgHeight}
        />

        <NumberField 
          key="underground-storage-area"
          title="Общая площадь кладовых помещений в м²"
          value={undergroundStorageArea}
          placeholder='1'
          onChange={setUndergroundStorageArea}
        />

        <CheckboxField 
          key="underground-parking"
          title="Наличие встроенной подземной стоянки автомобилей закрытого типа" 
          value={hasUndergroundParking} 
          onChange={setHasUndergroundParking} 
          inline={true}
        />

        <NumberField 
          key="underground-total-area"
          title="Общая площадь в м²"
          value={undergroundTotalArea}
          placeholder='1'
          onChange={setUndergroundTotalArea}
        />
        
        <NumberField 
          key="underground-gns-area"
          title="Площадь ГНС м²"
          value={undergroundGnsArea}
          placeholder='1'
          onChange={setUndergroundGnsArea}
        />
        
        <NumberField 
          key="underground-volume"
          title="Строительный объем в м³"
          value={undergroundVolume}
          placeholder='1'
          onChange={setUndergroundVolume}
        />
        
        <NumberField 
          key="underground-stairs"
          title="Количество лестничных клеток"
          value={undergroundStairs}
          placeholder='1'
          onChange={setUndergroundStairs}
        />
        
        <NumberField 
          key="underground-smokeless-stairs"
          title="Количество незадымляемых лестничных клеток"
          value={undergroundSmokelessStairs}
          placeholder='1'
          onChange={setUndergroundSmokelessStairs}
        />

        <div key="final-underground-question" className={styles.finalCorpusQuestion} style={{ gridColumn: 'span 2' }}>
          <div className={styles.leftPart}>
            <NumberField
              key="parking-floors"
              title="Этажи размещения стоянки автомобилей" 
              value={parkingFloors}
              onChange={setParkingFloors}
              placeholder="1"
            />

            <NumberField
              key="parking-tiers"
              title="Количество ярусов хранения автомобилей" 
              value={parkingTiers}
              onChange={setParkingTiers}
              placeholder="1"
            />

            <NumberField
              key="parking-total-area"
              title="Суммарная площадь стоянки автомобилей по всем этажам" 
              value={parkingTotalArea}
              onChange={setParkingTotalArea}
              placeholder="1"
            />
          </div>

          <div className={styles.rightPart}>
            <NumberField
              key="parking-fire-compartments"
              title="Количество пожарных отсеков, занимаемых стоянкой автомобилей" 
              value={parkingFireCompartments}
              onChange={setParkingFireCompartments}
              placeholder='1'
            />

            <NumberField
              key="parking-spaces"
              title="Количество машиномест" 
              value={parkingSpaces}
              onChange={setParkingSpaces}
              placeholder='1'
            />

            <CheckboxField
              key="has-car-wash"
              title="Наличие помещений мойки автомобилей в автостоянке" 
              value={hasCarWash} 
              onChange={setHasCarWash} 
              inline={false}
            />
          </div>
        </div>
      </NumberFieldsGrid>

      <h2 style={{ fontFamily: 'Montserrat' }}>Площади и типы фасадов</h2>
      <div className={styles.sliderContainer}>
        <Slider 
          title1="Глухая часть фасадов"
          title2="Светопрозрачные конструкции фасадов"
          sliderTitles1={[
            'Панель ж/б',
            'Кирпичная кладка',
            'Мокрый фасад (штукатурка)',
            'Плитка',
            'Кассеты металлические стальные',
            'Фиброцементные панели',
            'Кассеты композитные',
            'С стеклофибробетон'
          ]}
          sliderTitles2={[
            'Стеклопакет (в ПВХ раме)',
            'Стеклопакет (в алюминиевой раме)',
            'Входные группы'
          ]}
        />

        <CheckboxTrue 
          checked={objectCalculated}
          onChange={setObjectCalculated}
          label="Расчетные данные по объекту"
        />
      </div>

      <NumberFieldsGrid title="Расчетные данные по объекту">
        <NumberField 
          key="calculated-stairs"
          title="Количество незадымляемых лестничных клеток, обслуживающих надземную часть"
          value={calculatedStairs}
          placeholder='1'
          onChange={setCalculatedStairs}
        />

        <NumberField 
          key="calculated-elevators"
          title="Количество лифтов в здании (Надземной части, стилобатной части, пристроенных помещений)"
          value={calculatedElevators}
          placeholder='1'
          onChange={setCalculatedElevators}
        />

        <NumberField 
          key="calculated-staircases"
          title="Количество лестничных клеток, обслуживающие надземную часть"
          value={calculatedStaircases}
          placeholder='1'
          onChange={setCalculatedStaircases}
        />

        <NumberField 
          key="calculated-public-area"
          title="Суммарная площадь общественных помещений на объекте"
          value={calculatedPublicArea}
          placeholder='1'
          onChange={setCalculatedPublicArea}
        />

        <NumberField 
          key="calculated-public-purpose"
          title="Назначение встроенных общественных помещений"
          value={calculatedPublicPurpose}
          placeholder='1'
          onChange={setCalculatedPublicPurpose}
        />

        <NumberField 
          key="calculated-public-count"
          title="Количество общественных помещений"
          value={calculatedPublicCount}
          placeholder='1'
          onChange={setCalculatedPublicCount}
        />

        <NumberField 
          key="calculated-aboveground-volume"
          title="Строительный объем надземной части здания"
          value={calculatedAbovegroundVolume}
          placeholder='1'
          onChange={setCalculatedAbovegroundVolume}
        />

        <NumberField 
          key="calculated-residents"
          title="Количество жителей объекта"
          value={calculatedResidents}
          placeholder='1'
          onChange={setCalculatedResidents}
        />

        <NumberField 
          key="calculated-underground-volume"
          title="Строительный объем подземной части здания"
          value={calculatedUndergroundVolume}
          placeholder='1'
          onChange={setCalculatedUndergroundVolume}
        />
        <div></div>

        <NumberField 
          key="calculated-total-area"
          title="Общая площадь объекта"
          value={calculatedTotalArea}
          placeholder='1'
          onChange={setCalculatedTotalArea}
        />
        <div></div>

        <NumberField 
          key="calculated-total-volume"
          title="Строительный объем объекта"
          value={calculatedTotalVolume}
          placeholder='1'
          onChange={setCalculatedTotalVolume}
        />
        <div></div>

        <NumberField 
          key="calculated-residents-count"
          title="Количество жителей объекта"
          value={calculatedResidentsCount}
          placeholder='1'
          onChange={setCalculatedResidentsCount}
        />
      </NumberFieldsGrid>
    </div>
  );
}
